# 导入必要的模块和自定义工具包
from os import getcwd, startfile, path
from os.path import exists
from pathlib import Path
from re import search
from shutil import rmtree
from subprocess import CalledProcessError, run
from winreg import (
    OpenKey, SetValueEx, HKEY_LOCAL_MACHINE,
    REG_SZ, KEY_SET_VALUE
)
from zipfile import ZipFile

from DownloadKit import DownloadKit  # 自定义下载工具类

from config import Config
from log import Logger

# 配置参数
MIRROR_URL = "https://mirrors.tuna.tsinghua.edu.cn/Adoptium/21.0.3+9/"
VERSION = "21.0.3_9"
INSTALL_DIR = Path(r"C:\Program Files\Java")
TEMP_FILE = Path.home() / "jdk_temp.zip"

config = Config()
logger = Logger(__name__)

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

def check_java_version():
    """
    检测系统中是否存在Java 17及以上版本。

    Returns:
        bool: 如果存在Java 17及以上版本，则返回True；否则返回False。
    """
    try:
        # 尝试运行java -version命令
        process = run(['java', '-version'], capture_output=True, text=True, check=True)
        output = process.stderr  # Java version information usually goes to stderr

        # 使用正则表达式提取版本号
        match = search(r'version "(.*?)"', output)
        if match:
            version_string = match.group(1)
            # 将版本号分割成主要、次要和修订版本号
            version_parts = version_string.split('.')

            # 检查是否是 Java 17 或更高版本 (JDK 9 之后版本号方案改变)
            if version_parts[0] == '17' or (len(version_parts) > 0 and int(version_parts[0]) > 17):
                return True  # Java 17或更高版本
            elif version_parts[0] == '1': # JDK 8及更早版本
                if len(version_parts) > 1 and int(version_parts[1]) >= 7: # Java 7以上
                    return True
                else:
                    return False
            else:
                return False # Java 6或更早版本

        # 检查OpenJDK格式版本号（例如：17.0.2+8-Ubuntu-122.04.1）
        match = search(r'openjdk version "(.*?)"', output)
        if match:
            version_string = match.group(1)
            version_parts = version_string.split('.')
            if len(version_parts) >= 2 and int(version_parts[0]) >= 17:
                return True
            else:
                return False

        return False  # 无法解析版本号

    except FileNotFoundError:
        # java命令不存在
        logger.error("java不存在")
        return False
    except CalledProcessError as e:
        # java命令执行出错
        logger.error(f"在查询java版本时出现了问题: {e}")
        return False
    except Exception as e:
        # 其他异常
        logger.error(f"发生了意想不到的错误: {e}")
        return False

# 配置参数
ARCHITECTURE = "x64" if path.exists("C:\\Program Files (x86)") else "x86"
INSTALLER_FILENAME = f"OpenJDK{VERSION}-{ARCHITECTURE}_msi.zip"
INSTALL_DIR = Path(r"C:\Program Files\Java")
JAVA_INSTALLER_PATH = INSTALL_DIR / f"jdk-{VERSION}.msi"


def download_java_installer():
    """下载Java安装包"""
    d = DownloadKit(INSTALL_DIR)
    url = f"{MIRROR_URL}{INSTALLER_FILENAME}"
    d.download(url, file_exists="overwrite", show_msg=True)


def extract_installer():
    """解压下载的安装包至指定目录"""
    with ZipFile(INSTALL_DIR / INSTALLER_FILENAME, 'r') as zip_ref:
        zip_ref.extractall(INSTALL_DIR)
    logger.info(f"安装包 {INSTALLER_FILENAME} 解压完成")


def register_java_in_registry():
    """在注册表中注册Java路径以便系统识别"""
    try:
        key_path = r"SOFTWARE\JavaSoft\Java Development Kit"
        with OpenKey(HKEY_LOCAL_MACHINE, key_path, access=KEY_SET_VALUE) as key:
            SetValueEx(key, "CurrentVersion", 0, REG_SZ, VERSION)
            java_home = str(INSTALL_DIR / f"jdk-{VERSION}")
            SetValueEx(key, "JavaHome", 0, REG_SZ, java_home)
        logger.info("Java已成功注册到系统注册表")
    except Exception as e:
        logger.error(f"注册表操作失败: {e}")


def silent_install_java():
    """执行Java的静默安装"""
    try:
        command = [JAVA_INSTALLER_PATH, "/i", "/qn"]
        run(command, check=True)
        logger.info("Java已静默安装完成")
    except CalledProcessError as e:
        logger.error(f"Java安装过程中发生错误: {e}")
    except FileNotFoundError:
        logger.error("找不到Java安装文件，请确保正确下载并解压")


def install_java():
    """主函数：下载、解压、安装Java，并注册至系统"""
    logger.info("开始下载Java安装包...")
    download_java_installer()
    logger.info("下载完成，开始解压...")
    extract_installer()
    logger.info("准备安装Java...")
    silent_install_java()
    logger.info("安装完毕，正在注册至系统注册表...")
    register_java_in_registry()

