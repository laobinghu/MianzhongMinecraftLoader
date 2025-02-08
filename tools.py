# 导入必要的模块和自定义工具包
from os import getcwd, startfile
from os.path import exists
from time import sleep
from zipfile import ZipFile
from DownloadKit import DownloadKit  # 自定义下载工具类
from sys import exc_info
from shutil import rmtree
from config import Config

config = Config()

# 下载函数，使用DownloadKit工具进行文件下载
def Download():
    """下载启动器压缩包"""
    d = DownloadKit(r'.\tmp')
    d.download(config.LauncherUrl, file_exists="overwrite", show_msg=True)


# 解压函数，解压之前下载的ZIP文件到指定目录
def Unzip():
    """解压ZIP文件至当前工作目录"""
    zip_path = getcwd() + r'\tmp\launcher.zip'
    extract_folder = ''  # 注意：此处应指定实际提取路径或修正为适当值
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
        print("ZIP文件解压完成")


# 启动函数，执行启动器exe文件
def Open():
    """打开启动器应用程序"""
    exe_path = getcwd() + r"\launcher\Plain Craft Launcher 2.exe"
    startfile(exe_path)


# 检查启动器是否已存在
def check_launcher_exists():
    """检查指定路径下的启动器是否存在"""
    return exists(r".\launcher\Plain Craft Launcher 2.exe")


# 强制更新操作，删除旧的临时文件及启动器目录
def force_update():
    """执行强制更新，删除tmp和launcher目录"""
    rmtree(r".\tmp", ignore_errors=True)
    rmtree(r".\launcher", ignore_errors=True)



# 主程序入口
if __name__ == "__main__":
    # 打印欢迎及版本信息
    print(r"""
  __  __                         ___   ____  
 |  \/  | ____ _ __ ___    ___  / _ \ / ___| 
 | |\/| ||_  /| '_ ` _ \  / __|| | | |\___ \ 
 | |  | | / / | | | | | || (__ | |_| | ___) |
 |_|  |_|/___||_| |_| |_| \___| \___/ |____/                                              
=============================================
            Ver CUI Dev 0.0.2
Tip:已下载的文件会被覆盖                                
""")

    # 判断必要文件是否存在以决定是否需要下载和解压
    if exists(r'.\tmp\launcher.zip') and exists(r".\launcher\Plain Craft Launcher 2.exe"):
        print("整合包已存在,跳过下载")
        sleep(1)
        print("启动器已存在,进入启动环节")
        sleep(1)
        print("enjoy")
        sleep(1)
        Open()
    else:
        UserInput = input("键入yes以开始下载\n")
        match UserInput:
            case "yes":
                try:
                    # 检查并下载、解压启动器
                    if not exists(r'.\tmp\launcher.zip'):
                        Download()
                        sleep(1)
                    else:
                        print("整合包已存在,跳过下载")
                        sleep(1)
                    if not exists(r".\launcher\Plain Craft Launcher 2.exe"):
                        Unzip()
                        sleep(1)
                    else:
                        print("启动器已存在,进入启动环节")
                        sleep(1)
                except Exception as e:
                    print(f"出错了qwq{e}")
                    print(f"异常信息：{exc_info()}")
                    print("请截图发给管理员")
                    sleep(5)
                else:
                    print("enjoy")
                    sleep(1)
                    Open()
            case _:
                print("下次再见。")
                sleep(1)
                pass