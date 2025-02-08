# 导入日志模块
import logging
from time import strftime,localtime

# 设置日志模块的基本配置，级别为INFO，格式为：[日志级别][时间]: 日志信息
logging.basicConfig(level=logging.INFO, format='[%(levelname)s][%(asctime)s]: %(message)s',filename='loader.log',filemode='a',)


# 定义一个Logger类来封装日志操作
class Logger:
    # 初始化方法，根据传入的name创建并配置logger实例
    def __init__(self, name):
        # 使用logging.getLogger(name)获取或创建一个logger实例
        self.logger = logging.getLogger(name)
        # 设置logger实例的日志级别为INFO
        self.logger.setLevel(logging.INFO)

    # info方法，记录info级别的日志
    def info(self, message):
        self.logger.info(message)

    # warning方法，记录warning级别的日志
    def warning(self, message):
        self.logger.warning(message)

    # error方法，记录error级别的日志
    def error(self, message):
        self.logger.error(message)