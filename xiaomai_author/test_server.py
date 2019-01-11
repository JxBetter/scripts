import time
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/getUserInfo', methods=['POST'])
def platform():
    print(request.form)
    time.sleep(3)
    rsp = {
    "result": 1,
    "code": "SUCCESS",
    "msg": "success",
    "data": {
        "user": {
            "userGuid": "1",
            "username": "1",
            "password": "1",
            "createTime": "2019-01-10 18:12:43",
            "modifyTime": "2019-01-10 18:12:43"
        },
        "faceCapacityDtoList": [
            {
                "faceCapacityName": "5000容量",
                "allowNum": 15,
                "consumeNum": 1
            },
            {
                "faceCapacityName": "3000容量",
                "allowNum": 20,
                "consumeNum": 10
            }
        ]
    }
}
    return jsonify(rsp)


@app.route('/getDeviceCapacity')
def get_capacity():
    print(request.form)
    time.sleep(3)
    res = {"data":'{"sn":"84E0F42055C502FA","capacity":"5000"}',"result":0,"success":True}
    return jsonify(res)


@app.route('/setDeviceCapacity', methods=['POST'])
def set_capacity():
    print(request.form)
    time.sleep(3)
    res = {"msg":"success","result":1,"success":True}
    return jsonify(res)


if __name__ == '__main__':
    app.run(host='192.168.12.57', port=8090)