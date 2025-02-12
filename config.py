# 导入所需库
from json import loads
from requests import request
from mid import generate_mid


class Config:
    def __init__(self):
        # 初始化配置属性
        self.ReleaseCode = "通慧"  # 发布代码标识
        self.VersionType = "Release"  # 版本类型（开发版、正式版等）
        self.MajorVersionNum = 2  # 主版本号
        self.MinorVersionNum = 5  # 次版本号
        self.RevisionVersionNum = 0  # 修订版本号
        self.DateVersionNum = "202502012"  # 日期版本号
        self.version = None  # 完整版本字符串，初始化为空

        # 设置请求远程配置的URL和头部信息
        self.url = "https://mx.647382.xyz/api/v2/snippets/mzmcos/loader"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"}  # HTTP请求头模拟浏览器

        # 初始化网络请求响应和服务器配置变量
        self.response = None
        self.ServerConfig = None

        # 启动器下载链接
        self.LauncherUrl = 'https://cdn.647382.xyz/mzmcos/launcher.zip'

        self.MID = generate_mid()

    def GetVersion(self,builder=False):
        """生成并返回完整版本字符串"""
        version_fields = {
            'ReleaseCode': self.ReleaseCode,
            'VersionType': self.VersionType,
            'MajorVersionNum': self.MajorVersionNum,
            'MinorVersionNum': self.MinorVersionNum,
            'RevisionVersionNum': self.RevisionVersionNum,
            'DateVersionNum': self.DateVersionNum
        }
        # 根据字段拼接版本字符串
        if builder:
            self.version = list()
            self.version.append(self.MajorVersionNum)
            self.version.append(self.MinorVersionNum)
            self.version.append(self.RevisionVersionNum)
            self.version.append(int(self.DateVersionNum))
            return self.version
        else:
            self.version = f"{version_fields['ReleaseCode']} {version_fields['VersionType']} {version_fields['MajorVersionNum']}.{version_fields['MinorVersionNum']}.{version_fields['RevisionVersionNum']}-{version_fields['DateVersionNum']}"
            return self.version

    def GetInfo(self):
        """预留方法，用于获取其他配置信息，当前未实现"""
        pass

    def GetMID(self):
        return self.MID

    def GetServerConfig(self):
        """从远程服务器获取配置数据的方法"""
        self.response = request("GET", self.url, headers=self.headers)
        # 解析响应内容为JSON格式并返回
        return loads(self.response.text)

    def handle_server_config(self):
        """尝试获取服务器配置，包含异常处理逻辑"""
        try:
            # 调用GetServerConfig获取配置，并设置到实例变量中
            self.ServerConfig = self.GetServerConfig()
            return self.ServerConfig
        except Exception:
            # 如果请求过程中发生错误，则返回None
            return None

    def GetJavaUrl(self):
        return self.JavaUrl

# 主程序入口
if __name__ == "__main__":
    # 创建Config类的实例
    config = Config()
    # 打印生成的版本信息
    print(config.GetVersion())