from os import getcwd, startfile
from os.path import exists
from json import loads
from time import sleep
from zipfile import ZipFile
from requests import request
from DownloadKit import DownloadKit
from sys import exc_info



def Download():
    d = DownloadKit(r'.\tmp')
    url1 = 'https://cdn.647382.xyz/mzmcos/launcher.zip'
    d.download(url1, file_exists="overwrite", show_msg=True)


def Unzip():
    zip_path = getcwd() + r'\tmp\launcher.zip'
    extract_folder = ''

    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
        print("ZIP文件解压完成")


def Open():
    exe_path = getcwd() + r"\launcher\Plain Craft Launcher 2.exe"
    startfile(exe_path)


def GetServerConfig():
    url = "https://mx.647382.xyz/api/v2/snippets/mzmcos/loader"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"}
    response = request("GET", url, headers=header)

    ServerConfig = loads(response.text)

    return ServerConfig


if __name__ == "__main__":
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
                    print("出错了qwq{}".format(e))
                    print("异常信息：{}".format(exc_info()))
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

