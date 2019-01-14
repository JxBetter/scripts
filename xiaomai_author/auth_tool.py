import btn_logic
from tkinter import *

ui_global = {}


def create_ui():
    """
    创建界面
    :return:
    """
    root = Tk()

    root.title('Uface照片容量授权工具')
    root.geometry('600x350')
    root.resizable(0, 0)

    Label(root, text='账号：').place(x=30, y=40)
    Label(root, text='密码：').place(x=30, y=70)
    Label(root, text='设备IP：').place(x=30, y=100)

    v1 = StringVar()
    v2 = StringVar()
    v3 = StringVar()

    e1 = Entry(root, textvariable=v1)
    e2 = Entry(root, textvariable=v2)
    e3 = Entry(root, textvariable=v3)

    e1.place(x=100, y=40)
    e2.place(x=100, y=70)
    e3.place(x=100, y=100)

    w = Canvas(root, width=450, height=160)
    w.place(x=40, y=150)

    w.create_line(0, 0, 450, 0, fill="#000", width=5)
    w.create_line(0, 0, 0, 160, fill="#000", width=5)
    w.create_line(0, 160, 450, 160, fill="#000", width=1)
    w.create_line(450, 160, 450, 0, fill="#000", width=1)

    w.create_line(150, 0, 150, 200, fill="#000", width=1)
    w.create_line(300, 0, 300, 200, fill="#000", width=1)
    w.create_line(0, 40, 450, 40, fill="#000", width=1)
    w.create_line(0, 80, 450, 80, fill="#000", width=1)
    w.create_line(0, 120, 450, 120, fill="#000", width=1)
    w.create_line(0, 160, 450, 160, fill="#000", width=1)

    Label(root, text='照片容量类型').place(x=80, y=160)
    Label(root, text='授权数量').place(x=238, y=160)
    Label(root, text='操作').place(x=400, y=160)
    Label(root, text='1000').place(x=100, y=200)
    Label(root, text='2000').place(x=100, y=240)
    Label(root, text='5000').place(x=100, y=280)

    v4 = StringVar()
    v5 = StringVar()
    v6 = StringVar()

    e4 = Entry(root, textvariable=v4, width=12, state='readonly')
    e5 = Entry(root, textvariable=v5, width=12, state='readonly')
    e6 = Entry(root, textvariable=v6, width=12, state='readonly')

    e4.place(x=220, y=200)
    e5.place(x=220, y=240)
    e6.place(x=220, y=280)

    Button(root, text='查询设备人脸容量', width=15, command=lambda: btn_logic.get_capacity_btn_main(ui_global)).place(x=280,
                                                                                                              y=110)
    Button(root, text='刷新', width=10, command=lambda: btn_logic.refresh_btn_main(ui_global)).place(x=410, y=110)
    Button(root, text='授权', width=10, command=lambda: btn_logic.auth_btn_main(ui_global, '1000')).place(x=380, y=195)
    Button(root, text='授权', width=10, command=lambda: btn_logic.auth_btn_main(ui_global, '2000')).place(x=380, y=235)
    Button(root, text='授权', width=10, command=lambda: btn_logic.auth_btn_main(ui_global, '5000')).place(x=380, y=275)

    ui_global['flag'] = True
    ui_global['account'] = e1
    ui_global['pwd'] = e2
    ui_global['ip'] = e3
    ui_global['v4'] = v4
    ui_global['v5'] = v5
    ui_global['v6'] = v6

    mainloop()


if __name__ == '__main__':
    create_ui()
