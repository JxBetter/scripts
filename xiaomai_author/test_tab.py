import requests

import tkinter
from tkinter import ttk  # 导入内部包
from tkinter import *
from PyInstaller.__main__ import run

win = tkinter.Tk()
tree = ttk.Treeview(win)  # 表格
tree["columns"] = ("姓名", "年龄", "身高")
tree.column("姓名", width=100)  # 表示列,不显示
tree.column("年龄", width=100)
tree.column("身高", width=100)

tree.heading("姓名", text="姓名-name")  # 显示表头
tree.heading("年龄", text="年龄-age")
tree.heading("身高", text="身高-tall")


b = Button(win, text='授权', width=10)

tree.insert("", 0, text="line1", values=("1", "2", b))  # 插入数据，
tree.insert("", 1, text="line1", values=("1", "2", "3"))
tree.insert("", 2, text="line1", values=("1", "2", "3"))
tree.insert("", 3, text="line1", values=("1", "2", "3"))

tree.pack()

# tkinter.mainloop()

r = requests.get('http://192.168.12.123:8090/getDeviceKey')
print(type(r.text))