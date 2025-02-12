from tkinter import Tk, StringVar, IntVar, messagebox
from tkinter.ttk import Progressbar, Label
from PIL import Image, ImageTk
from time import sleep
from os.path import exists
from sys import exc_info
from threading import Thread
from typing import Optional, Dict

from tools import (
    Download,
    Unzip,
    Open,
    check_launcher_exists,
    force_update,
    check_java_version,
    install_java
)
from config import Config
from log import Logger


class UIConstants:
    """UI配置常量类"""
    WINDOW_TITLE = "MianzhongMinecraftLoader"
    WINDOW_SIZE = (400, 250)
    BACKGROUND = "white"
    GEOMETRY_FORMAT = "%dx%d+%d+%d"
    IMAGE_PATH = "./asset/img.png"
    ICON_PATH = "./asset/loader.ico"
    PROGRESS_LAYOUT = {
        "relx": 0.0,
        "rely": 0.8,
        "relwidth": 1.0,
        "relheight": 0.12
    }
    LABEL_LAYOUT = {
        "relx": 0.15,
        "rely": 0.56,
        "relwidth": 0.7,
        "relheight": 0.16
    }
    IMAGE_LAYOUT = {
        "relx": 0.0075,
        "rely": 0.1,
        "relwidth": 1,
        "relheight": 0.5
    }


class JavaInstallFailedError(Exception):
    """Java环境安装失败异常"""
    pass


class MinecraftLoader:
    def __init__(self, master: Tk):
        self.master = master
        self.config = Config()
        self.logger = Logger(__name__)

        self._init_window()
        self._create_widgets()
        self._load_resources()
        self.logger.info("Minecraft Loader 初始化完成")

    def _init_window(self):
        """初始化窗口配置"""
        self.master.title(UIConstants.WINDOW_TITLE)
        self.master.iconbitmap(UIConstants.ICON_PATH)
        self.master.configure(background=UIConstants.BACKGROUND)

        width, height = UIConstants.WINDOW_SIZE
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        geometry = UIConstants.GEOMETRY_FORMAT % (
            width,
            height,
            (screen_width - width) // 2,
            (screen_height - height) // 2
        )
        self.master.geometry(geometry)
        self.master.minsize(width=width, height=height)

    def _create_widgets(self):
        """创建界面组件"""
        # 进度条
        self.progress_value = IntVar(value=0)
        self.progressbar = Progressbar(
            self.master,
            variable=self.progress_value
        )
        self.progressbar.place(**UIConstants.PROGRESS_LAYOUT)

        # 信息标签
        self.info_text = StringVar(value=self.config.GetVersion())
        self.info_label = Label(
            self.master,
            textvariable=self.info_text,
            anchor="center",
            background=UIConstants.BACKGROUND
        )
        self.info_label.place(**UIConstants.LABEL_LAYOUT)

    def _load_resources(self):
        """加载图片资源"""
        try:
            img = Image.open(UIConstants.IMAGE_PATH).resize((360, 90))
            self.logo_image = ImageTk.PhotoImage(img)
            self.logger.info(f"成功加载图片: {UIConstants.IMAGE_PATH}")
        except FileNotFoundError:
            self.logger.error(f"图片文件未找到: {UIConstants.IMAGE_PATH}")
            self.logo_image = None

        # 图片标签
        self.image_label = Label(
            self.master,
            image=self.logo_image,
            anchor="center",
            background=UIConstants.BACKGROUND
        )
        self.image_label.place(**UIConstants.IMAGE_LAYOUT)

    def _update_ui(self, progress: int, message: str):
        """统一更新界面元素"""
        self.progress_value.set(progress)
        self.info_text.set(message)
        self.logger.info(f"UI更新 - 进度: {progress}% | 信息: {message}")

    def _simulate_network_communication(self):
        """模拟网络通信流程"""
        steps = [
            (10, "与服务器通信中"),
            (20, "Action"),
            (30, "Emotion"),
            (100, "通信完成")
        ]
        for progress, message in steps:
            self._update_ui(progress, message)
            sleep(0.3)

    def _validate_java_installation(self):
        """验证Java安装结果"""
        if check_java_version():
            self._update_ui(40, "Java环境校验通过")
            sleep(0.5)
        else:
            raise JavaInstallFailedError("Java安装后校验失败")

    def _install_java(self):
        """执行Java安装流程"""
        self._update_ui(30, "开始安装Java")
        install_java()
        self._update_ui(40, "正在验证安装结果")

    def _handle_config_error(self):
        """处理配置错误"""
        error_msg = "API请求异常，请检查服务器状态"
        self.logger.error(error_msg)
        self._update_ui(0, error_msg)
        sleep(2)
        self._safe_shutdown()

    def _force_update_launcher(self):
        """处理强制更新流程"""
        force_update()
        self._update_ui(60, "启动器强制更新中")
        self._download_launcher()
        self._finalize_launcher()

    def _normal_update_launcher(self):
        """处理常规更新流程"""
        if check_launcher_exists():
            self._update_ui(90, "启动器已就绪")
            sleep(1)
            self._launch_game()
        else:
            self._confirm_download()

    def _confirm_download(self):
        """用户确认下载流程"""
        confirm = messagebox.askquestion(
            "确认下载",
            "未检测到启动器，是否现在下载？"
        )
        if confirm == "yes":
            self._download_launcher()
            self._finalize_launcher()
        else:
            self._update_ui(100, "操作已取消")
            self.logger.info("用户取消下载")
            sleep(1)
            self._safe_shutdown()

    def _download_launcher(self):
        """执行启动器下载"""
        if not exists(r".\tmp\launcher.zip"):
            self._update_ui(60, "开始下载启动器")
            Download()
            sleep(0.5)
        else:
            self._update_ui(60, "使用本地缓存文件")
            sleep(0.5)

    def _finalize_launcher(self):
        """完成启动器安装"""
        if not check_launcher_exists():
            self._update_ui(80, "解压启动器文件")
            Unzip()
        self._update_ui(100, "准备就绪")
        self._launch_game()

    def _launch_game(self):
        """启动游戏"""
        self._update_ui(100, "正在启动...")
        Open()
        sleep(1)
        self._safe_shutdown()

    def _safe_shutdown(self):
        """安全关闭程序"""
        self.master.after(400, self.master.destroy)

    def main_loop(self):
        """主业务流程"""
        try:
            self._simulate_network_communication()

            # 检查Java环境
            if not check_java_version():
                self._install_java()
            self._validate_java_installation()

            # 处理启动器逻辑
            server_config = self.config.handle_server_config()
            if not server_config:
                self._handle_config_error()
                return

            if server_config["launcher"].get("ForceDownload") == "true":
                self._force_update_launcher()
            else:
                self._normal_update_launcher()

        except JavaInstallFailedError as e:
            self.logger.exception("Java安装失败")
            messagebox.showerror("严重错误", "Java环境安装失败，程序将退出")
            self._safe_shutdown()
        except Exception as e:
            self.logger.exception("未处理的异常")
            self._update_ui(0, f"发生未知错误: {str(e)}")
            sleep(2)
            self._safe_shutdown()


if __name__ == "__main__":
    root = Tk()
    loader = MinecraftLoader(root)
    Thread(target=loader.main_loop).start()
    root.mainloop()
