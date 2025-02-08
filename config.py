from json import loads
from requests import request


class Config:
    def __init__(self):
        self.ReleaseCode = "通慧"
        self.VersionType = "Dev"
        self.MajorVersionNum = 2
        self.MinorVersionNum = 0
        self.RevisionVersionNum = 0
        self.DateVersionNum = "20250208"
        self.Meta = "ReBuilding"
        self.version = None

        self.url = "https://mx.647382.xyz/api/v2/snippets/mzmcos/loader"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"}
        self.response = None
        self.ServerConfig = None

        #self.

    def GetVersion(self):
        version_fields = {
            'ReleaseCode': self.ReleaseCode,
            'VersionType': self.VersionType,
            'MajorVersionNum': self.MajorVersionNum,
            'MinorVersionNum': self.MinorVersionNum,  # 修正此处的 Self 为 self 并移除多余的 VersionNum
            'RevisionVersionNum': self.RevisionVersionNum,
            'DateVersionNum': self.DateVersionNum,
            'Meta': self.Meta
        }
        self.version = f"{version_fields['ReleaseCode']} {version_fields['VersionType']} {version_fields['MajorVersionNum']}.{version_fields['MinorVersionNum']}.{version_fields['RevisionVersionNum']}-{version_fields['DateVersionNum']}~{version_fields['Meta']}"
        return self.version

    def GetInfo(self):
        pass

    # 获取服务器配置信息
    def GetServerConfig(self):
        """从远程服务器获取配置数据"""
        self.response = request("GET", self.url, headers=self.headers)
        return loads(self.response.text)

    # 处理服务器配置逻辑，包含异常处理
    def handle_server_config(self):
        """尝试获取服务器配置并处理异常"""
        try:
            self.ServerConfig = self.GetServerConfig()
            return self.ServerConfig
        except Exception:
            return None

if __name__ == "__main__":
    config = Config()
    print(config.GetVersion())