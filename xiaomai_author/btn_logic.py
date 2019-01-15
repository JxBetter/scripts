import json
import time
import requests
import threading
from hashlib import md5
from tkinter import ttk, messagebox


def get_num_of_face_type_from_platform(account, pwd):
    """
    从平台获取账号下人脸容量的授权数
    :param account: 账号
    :param pwd: 密码
    :return: 成功返回：数据, True
              失败返回：None, False
    """
    server_host = 'facecapacity.uni-ubi.com'
    url = 'http://{}/getUserInfo'.format(server_host)
    data = {
        'username': account,
        'password': pwd
    }
    try:
        r = requests.post(url, data, timeout=3)
    except Exception as e:
        messagebox.showinfo(message='网络异常请检查网络')
        return None, False
    else:
        if (json.loads(r.text)['code'] == 'SUCCESS'):
            return json.loads(r.text)['data']['faceCapacityDtoList'], True
        else:
            messagebox.showinfo(message=json.loads(r.text).get('msg', '出现了未知错误~'))
            return None, False


def get_device_key_and_current_capacity_from_android(ip):
    """
    从设备端获取序列号和设备当前人脸容量
    :param ip: 设备ip
    :return: 成功返回：数据, True
              失败返回：None, False
    """
    url = 'http://{}:8090/getDeviceCapacity'.format(ip)
    try:
        r = requests.get(url, timeout=3)
    except Exception as e:
        messagebox.showinfo(message='网络异常请检查网络')
        return None, False
    else:
        if (r.status_code != 200):
            messagebox.showinfo(message='设备不支持设置或查询人脸容量')
            return None, False
        if (json.loads(r.text)['success'] is False):
            messagebox.showinfo(message=json.loads(r.text).get('msg', '出现了未知错误~'))
            return None, False
        return [json.loads(r.text)['data']['capacity'],
                json.loads(r.text)['data']['sn']], True


def check_rest_of_capacity(face_capacity_list, face_capacity_type):
    """
    检查人脸容量的授权数是否大于0
    :param face_capacity_list: 平台返回的人脸类型授权数列表
    :param face_capacity_type: 需要授权的人脸容量数
    :return: 大于0：True
              小于等于0：False
    """
    for ele in face_capacity_list:
        if (face_capacity_type in ele['faceCapacityName']):
            return ele['allowNum'] - ele['consumeNum'] > 0


def create_sign(account, pwd, sn, device_capacity):
    """
    创建验证签名
    :param account: 账号
    :param pwd: 密码
    :param sn: 设备序列号
    :param device_capacity: 需要授权的人脸容量数
    :return:
    """
    timestamp = str(int(time.time() * 1000))

    mdfive = md5()
    account_pwd_md5 = md5()

    account_pwd_md5.update((account + pwd).encode())
    mdfive.update((account_pwd_md5.hexdigest() + sn + timestamp + str(device_capacity)).encode())
    return mdfive.hexdigest(), timestamp


def send_capacity_num_2_android(ip, account, pwd, sn, timestamp, face_capacity, sign):
    """
    设置设备人脸容量
    :param ip: 设备ip
    :param account: 账号
    :param pwd: 密码
    :param sn: 序列号
    :param timestamp: 毫秒级时间戳
    :param face_capacity: 需要授权的人脸容量
    :param sign: 验证签名
    :return: 成功返回：True
              失败返回：False
    """
    url = 'http://{}:8090/setDeviceCapacity'.format(ip)
    config_json = {
        'account': account,
        'password': pwd,
        'sn': sn,
        'currentTimeMillis': timestamp,
        'capacity': face_capacity,
        'sign': sign
    }
    data = {
        'config': json.dumps(config_json)
    }

    try:
        r = requests.post(url, data)
    except Exception as e:
        messagebox.showinfo(message='与设备通信失败，请检查设备是否正常开启')
        return False
    else:
        if (json.loads(r.text)['success'] is False):
            messagebox.showinfo(message=json.loads(r.text).get('msg', '出现了未知错误~'))
            return False
        else:
            return True


def get_capacity_btn(ip):
    """
    :param ip: 设备ip
    :return:
    """
    data, f = get_device_key_and_current_capacity_from_android(ip)
    if (f is False):
        return
    else:
        messagebox.showinfo(message='设备当前人脸容量为{}'.format(data[0]))


def get_capacity_btn_main(ui_global):
    "获取设备容量按钮"
    t = threading.Thread(target=get_capacity_btn, args=[ui_global['ip'].get()])
    t.start()


def refresh_btn(v4, v5, v6, account, pwd):
    """
    :param v4: 照片类型为500的授权数量控件
    :param v5: 照片类型为1000的授权数量控件
    :param v6: 照片类型为2000的授权数量控件
    :param account: 账号
    :param pwd: 密码
    :return:
    """
    data, f = get_num_of_face_type_from_platform(account, pwd)
    if (f is False):
        return
    else:
        for ele in data:
            if (ele['faceCapacityName'] == '1000容量'):
                v4.set('{}/{}'.format(ele['consumeNum'], ele['allowNum']))
            elif (ele['faceCapacityName'] == '2000容量'):
                v5.set('{}/{}'.format(ele['consumeNum'], ele['allowNum']))
            elif (ele['faceCapacityName'] == '5000容量'):
                v6.set('{}/{}'.format(ele['consumeNum'], ele['allowNum']))


def refresh_btn_main(ui_global):
    t = threading.Thread(target=refresh_btn,
                         args=[ui_global['v4'], ui_global['v5'], ui_global['v6'],
                               ui_global['account'].get(), ui_global['pwd'].get()])
    t.start()


def auth_btn(ui_global, face_capacity_type):
    """

    :param ui_global: ui全局变量，用来获取前端数据
    :param face_capacity_type: 需要授权的容量数
    :return:
    """
    if (ui_global['flag']):
        ui_global['flag'] = False
        # 1.从平台获取人脸容量授权数
        face_capacity_data, f1 = get_num_of_face_type_from_platform(ui_global['account'].get(), ui_global['pwd'].get())
        if (f1 is False):
            ui_global['flag'] = True
            return
        # 检查容量剩余授权数是否大于0
        f2 = check_rest_of_capacity(face_capacity_data, face_capacity_type)
        if (f2 is False):
            ui_global['flag'] = True
            messagebox.showinfo(message='{}人脸容量授权数不足 '.format(face_capacity_type))
            return
        # 2.从设备端获取序列号和设备当前人脸容量
        sn_capacity_data, f3 = get_device_key_and_current_capacity_from_android(ui_global['ip'].get())
        if (f3 is False):
            ui_global['flag'] = True
            return
        else:
            if (int(face_capacity_type) < int(sn_capacity_data[0])):
                messagebox.showinfo(message='当前设备人脸量为{}，无法降容授权为{}'.format(sn_capacity_data[0], face_capacity_type))
                ui_global['flag'] = True
                return
            elif (int(face_capacity_type) == int(sn_capacity_data[0])):
                messagebox.showinfo(message='当前设备人脸量为{}，无需重复授权'.format(sn_capacity_data[0]))
                ui_global['flag'] = True
                return
        # 3.生成签名
        sign, timestamp = create_sign(ui_global['account'].get(), ui_global['pwd'].get(), sn_capacity_data[1],
                                      face_capacity_type)
        # 4.设置设备人脸容量
        f4 = send_capacity_num_2_android(ui_global['ip'].get(), ui_global['account'].get(), ui_global['pwd'].get(),
                                         sn_capacity_data[1], timestamp, face_capacity_type, sign)
        if (f4 is False):
            ui_global['flag'] = True
            return
        else:
            # 5.设置成功后，再次从平台获取新的容量授权数，并更新显示界面
            data, f = get_num_of_face_type_from_platform(ui_global['account'].get(), ui_global['pwd'].get())
            if (f is False):
                ui_global['flag'] = True
                return
            else:
                for ele in data:
                    if (ele['faceCapacityName'] == '1000容量'):
                        ui_global['v4'].set('{}/{}'.format(ele['consumeNum'], ele['allowNum']))
                    elif (ele['faceCapacityName'] == '2000容量'):
                        ui_global['v5'].set('{}/{}'.format(ele['consumeNum'], ele['allowNum']))
                    elif (ele['faceCapacityName'] == '5000容量'):
                        ui_global['v6'].set('{}/{}'.format(ele['consumeNum'], ele['allowNum']))
                messagebox.showinfo(message='设备授权成功，目前人脸库为{}'.format(face_capacity_type))
        ui_global['flag'] = True
    else:
        messagebox.showinfo(message='授权中，请耐心等待')


def auth_btn_main(ui_global, face_capacity_type):
    "授权按钮"
    t = threading.Thread(target=auth_btn, args=[ui_global, face_capacity_type])
    t.start()


if __name__ == '__main__':
    r, s = create_sign('1', '1', '84E0F420533F02FA', '1000')
    print(r, s)
