class Config:
    def __init__(self):
        self.ReleaseCode = "通慧"
        self.VersionType = "Dev"
        self.MajorVersionNum = 2
        self.MinorVersionNum = 0
        self.RevisionVersionNum = 0
        self.DateVersionNum = "20250208"
        self.Meta = "ReBuilding"

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

if __name__ == "__main__":
    config = Config()
    print(config.GetVersion())