from os.path import exists
from shutil import rmtree
from tools import Download, Unzip, Open, GetServerConfig

def check_launcher_exists():
    """检查启动器是否存在"""
    return exists(r".\launcher\Plain Craft Launcher 2.exe")

def force_update():
    """强制更新启动器"""
    rmtree(r".\tmp", ignore_errors=True)
    rmtree(r".\launcher", ignore_errors=True)

def handle_server_config(value, info):
    """处理服务器配置"""
    try:
        ServerConfig = GetServerConfig()
        return ServerConfig
    except Exception as e:
        value.set(100)
        info.set("出错了qwq{}".format(e))
        info.set("异常信息：{}".format(exc_info()))
        return None
