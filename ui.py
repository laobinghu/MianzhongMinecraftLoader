import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from time import sleep
from os.path import exists
from sys import exc_info
from tkinter import messagebox
from threading import Thread

from tools import (Download, Unzip, Open, check_launcher_exists, force_update)
from config import Config
from log import Logger

config = Config()
logger = Logger(__name__)


class MinecraftLoader:
    """
    Minecraft启动器加载界面类。
    负责创建和管理加载界面，以及执行启动器的相关操作，如下载、解压和启动。
    """

    def __init__(self, master):
        """
        初始化MinecraftLoader类。

        Args:
            master: Tkinter的主窗口对象。
        """
        self.master = master
        master.title("MianzhongMinecraftLoader")
        master.iconbitmap(r'./asset/loader.ico')
        master.configure(bg="white")

        # 窗口大小和居中
        self.width = 400
        self.height = 250
        self.screenwidth = master.winfo_screenwidth()
        self.screenheight = master.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (
        self.width, self.height, (self.screenwidth - self.width) // 2, (self.screenheight - self.height) // 2)
        master.geometry(geometry)
        master.minsize(width=self.width, height=self.height)

        # 进度条
        self.value = tk.IntVar()
        self.value.set(0)
        self.progressbar = ttk.Progressbar(master, variable=self.value)
        self.progressbar.place(relx=0.0000, rely=0.8000, relwidth=1.0000, relheight=0.1200)

        # 信息标签
        self.info = tk.StringVar()
        self.info.set(config.GetVersion())

        # 加载图片
        try:
            img_open = Image.open(r'./asset/img.png').resize((360, 90))
            self.img_png = ImageTk.PhotoImage(img_open)
            logger.info("成功加载图片: ./asset/img.png")
        except FileNotFoundError:
            logger.error("图片文件未找到: ./asset/img.png")
            print("Error: Image file not found.  Using a placeholder.")
            self.img_png = None  # Or create a placeholder image.

        # 图片标签
        self.pic = ttk.Label(master, text="图片", anchor="center", image=self.img_png)
        self.pic.config(background="white")
        self.pic.place(relx=0.0075, rely=0.100, relwidth=1, relheight=0.5)

        # 信息标签
        self.label = ttk.Label(master, text="信息", anchor="center", textvariable=self.info)
        self.label.config(background="white")
        self.label.place(relx=0.1500, rely=0.5600, relwidth=0.7000, relheight=0.1600)
        logger.info("Minecraft Loader 初始化完成")

    def update_info(self, message):
        """更新信息标签"""
        self.info.set(message)
        logger.info(f"UI 信息更新: {message}")

    def update_progress(self, progress):
        """更新进度条"""
        self.value.set(progress)
        logger.info(f"进度条更新至: {progress}%")

    def main_loop(self):
        """主程序逻辑"""
        sleep(1)
        logger.info("与服务器通信中")

        self.update_info("与服务器通信中")
        sleep(0.3)
        self.update_info("Action")
        self.update_progress(10)
        sleep(0.3)

        ServerConfig = config.handle_server_config()
        if ServerConfig is None:
            logger.error("在请求API时发生了未知错误,请在群内询问API是否正常")
            self.update_info("在请求API时发生了未知错误,请在群内询问API是否正常")
            sleep(1)
            self.master.quit()
            self.master.destroy()
            return

        self.update_info("Response")
        self.update_progress(20)
        sleep(0.3)
        self.update_info("Emotion")
        self.update_progress(30)
        sleep(0.3)
        self.update_info("通信完成")
        logger.info("通信完成")

        if not ServerConfig["launcher"]["ForceDownload"] == "true" and check_launcher_exists():
            sleep(0.5)
            self.update_progress(90)
            self.update_info("启动器已存在,进入启动环节")
            logger.info("启动器已存在,进入启动环节")
            sleep(0.5)
            self.update_progress(100)
            self.update_info("enjoy")
            sleep(0.75)
            Open()
        elif ServerConfig["launcher"]["ForceDownload"] == "true" and check_launcher_exists():
            force_update()
            sleep(0.5)
            self.update_progress(60)
            self.update_info("启动器强制更新,开始下载")
            logger.info("启动器强制更新,开始下载")
            Download()
            sleep(0.5)
            self.update_progress(90)
            self.update_info("启动器已存在,进入启动环节")
            logger.info("启动器已存在,进入启动环节")
            sleep(0.5)
            self.update_progress(100)
            self.update_info("enjoy")
            sleep(0.75)
            Open()
        else:
            UserInput = messagebox.askquestion("我就问一下", "您还没有下载启动器,是否下载?")
            if UserInput == "yes":
                logger.info("用户选择下载启动器")
                try:
                    if not exists(r'.\tmp\launcher.zip'):
                        self.update_progress(60)
                        self.update_info("开始下载,请耐心等待,若长时间无反应请重试")
                        logger.info("开始下载启动器")
                        Download()
                        sleep(0.75)
                    else:
                        self.update_progress(60)
                        self.update_info("整合包已存在,跳过下载")
                        logger.info("整合包已存在,跳过下载")
                        sleep(0.75)
                    if not check_launcher_exists():
                        self.update_progress(90)
                        self.update_info("开始解压启动器")
                        logger.info("开始解压启动器")
                        Unzip()
                        sleep(0.75)
                    else:
                        self.update_progress(90)
                        self.update_info("启动器已存在,进入启动环节")
                        logger.info("启动器已存在,进入启动环节")
                        sleep(0.75)
                except Exception as e:
                    logger.error(f"未知错误: {e}, 异常详细信息: {exc_info()}")

                    self.update_info("出错了qwq{}".format(e))
                    sleep(1)
                    self.update_info("异常信息：{}".format(exc_info()))
                    sleep(1)
                else:
                    self.update_progress(100)
                    self.update_info("启动器加载中,请耐心等待")
                    logger.info("启动器加载中")
                    Open()
            else:
                self.update_progress(100)
                self.update_info("下次再见。")
                logger.info("用户取消下载，程序退出")
        self.master.after(400, self.master.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    loader = MinecraftLoader(root)
    Thread(target=loader.main_loop).start()
    root.mainloop()
