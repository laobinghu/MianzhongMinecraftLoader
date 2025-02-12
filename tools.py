# 导入必要的模块和自定义工具包
from os import getcwd, startfile, path, makedirs
from os.path import exists
from re import search
from shutil import rmtree
from subprocess import CalledProcessError
from subprocess import run
from zipfile import ZipFile

from DownloadKit import DownloadKit  # 自定义下载工具类
from setuptools.sandbox import save_path

from config import Config
from log import Logger

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
        match = search(r'openjdk "(.*?)"', output)
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
def install_java():
    # 配置下载参数
    file_url = 'https://cdn.647382.xyz/mzmcos/OpenJDK21U-jdk_x64_windows_hotspot_21.0.6_7.msi'
    save_path = getcwd() + r'\tmp\OpenJDK21U-jdk_x64_windows_hotspot_21.0.6_7.msi'
    # 初始化下载器
    downloader = DownloadKit(r'.\tmp')
    # 执行下载
    try:
        downloader.download(file_url,file_exists="overwrite", show_msg=True)
    except Exception as e:
        logger.error(f"下载失败: {str(e)}")
        raise JavaInstallFailedError
    else:
        logger.info(f"JDK下载成功")

    # 静默安装配置
    install_cmd = [
        'msiexec',
        '/i', save_path,
        '/qn',  # 完全静默模式
        '/norestart'  # 不强制重启
    ]

    # 执行安装
    try:
        run(install_cmd, check=True, shell=True)
        logger.info("Java 21已成功静默安装")
    except Exception as e:
        logger.error(f"安装失败: {str(e)}")
        raise JavaInstallFailedError
