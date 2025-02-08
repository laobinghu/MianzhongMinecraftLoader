from threading import Thread
from time import sleep
from os.path import exists
from sys import exc_info, exit
from tools import Download, Unzip, Open, GetServerConfig
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.ttk as ttk
from tkinter import messagebox
from shutil import rmtree

version = ["远志", "Release", "1.0.0"]

root = tk.Tk()
root.title("MianzhongMinecraftLoader")
root.iconbitmap(r'./asset/loader.ico')
root.configure(bg="white")
# 设置窗口大小、居中
width = 400
height = 250
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(geometry)
root.minsize(width=width, height=height)
value = tk.IntVar()
value.set(0)
progressbar = ttk.Progressbar(root, variable=value)
progressbar.place(relx=0.0000, rely=0.8000, relwidth=1.0000, relheight=0.1200)
info = tk.StringVar()
info.set("{0} {1} {2}".format(version[0], version[1], version[2]))

img_open = Image.open(r'./asset/img.png').resize((360, 90))

img_png = ImageTk.PhotoImage(img_open)

pic = ttk.Label(root, text="图片", anchor="center", image=img_png)
pic.config(background="white")
pic.place(relx=0.0075, rely=0.100, relwidth=1, relheight=0.5)
label = ttk.Label(root, text="信息", anchor="center", textvariable=info)
label.config(background="white")
label.place(relx=0.1500, rely=0.5600, relwidth=0.7000, relheight=0.1600)


def main():
    global ServerConfig
    sleep(1)
    info.set("与服务器通信中")
    sleep(0.3)
    info.set("Action")
    value.set(10)
    sleep(0.3)
    try:
        ServerConfig = GetServerConfig()
        sleep(0.2)
    except Exception as e:
        value.set(100)
        info.set("出错了qwq{}".format(e))
        sleep(1)
        info.set("异常信息：{}".format(exc_info()))
        sleep(1)
    else:
        info.set("Response")
        value.set(20)
        sleep(0.3)
    info.set("Emotion")
    value.set(30)
    sleep(0.3)
    info.set("通信完成")
    if not ServerConfig["launcher"]["ForceDownload"] == "true"\
            and exists(r".\launcher\Plain Craft Launcher 2.exe"):
        sleep(0.5)
        value.set(90)
        info.set("启动器已存在,进入启动环节")
        sleep(0.5)
        value.set(100)
        info.set("enjoy")
        sleep(0.75)
        Open()
    elif ServerConfig["launcher"]["ForceDownload"] == "true"\
            and exists(r".\launcher\Plain Craft Launcher 2.exe"):
        rmtree(r".\tmp", ignore_errors=True)
        rmtree(r".\launcher", ignore_errors=True)
        sleep(0.5)
        value.set(60)
        info.set("启动器强制更新,开始下载")
        Download()
        sleep(0.5)
        value.set(90)
        info.set("启动器已存在,进入启动环节")
        sleep(0.5)
        value.set(100)
        info.set("enjoy")
        sleep(0.75)
        Open()

    else:
        UserInput = messagebox.askquestion("我就问一下", "您还没有下载启动器,是否下载?")
        match UserInput:
            case "yes":
                try:
                    if not exists(r'.\tmp\launcher.zip'):
                        value.set(60)
                        info.set("开始下载,请耐心等待,若长时间无反应请重试")
                        Download()
                        sleep(0.75)
                    else:
                        value.set(60)
                        info.set("整合包已存在,跳过下载")
                        sleep(0.75)
                    if not exists(r".\launcher\Plain Craft Launcher 2.exe"):
                        value.set(90)
                        info.set("开始解压启动器")
                        Unzip()
                        sleep(0.75)
                    else:
                        value.set(90)
                        info.set("启动器已存在,进入启动环节")
                        sleep(0.75)
                except Exception as e:
                    info.set("出错了qwq{}".format(e))
                    sleep(1)
                    info.set("异常信息：{}".format(exc_info()))
                    sleep(1)
                else:
                    value.set(100)
                    info.set("启动器加载中,请耐心等待")
                    Open()
            case _:
                value.set(100)
                info.set("下次再见。")
                sleep(0.4)
    root.quit()
    root.destroy()


Thread(target=main).start()
root.mainloop()

exit()
