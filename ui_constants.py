class UIConstants:
    """UI配置常量类"""
    # 窗口设置
    WINDOW_TITLE = "Mianzhong Minecraft Loader"
    WINDOW_SIZE = (500, 320)
    GEOMETRY_FORMAT = "%dx%d+%d+%d"


    # 字体配置
    FONT_LABEL = ("微软雅黑", 14)
    MID_FONT_LABEL = ("微软雅黑", 8)
    FONT_TITLE = ("微软雅黑", 12, "bold")

    # 尺寸配置
    PROGRESS_HEIGHT = 25
    IMAGE_WIDTH = 450
    IMAGE_HEIGHT = 120

    # 路径配置
    IMAGE_PATH = "./asset/img.png"
    ICON_PATH = "./asset/loader.ico"

    # 布局参数
    PROGRESS_LAYOUT = {
        "relx": 0.05,
        "rely": 0.75,
        "relwidth": 0.9,
        "relheight": 0.08
    }
    LABEL_LAYOUT = {
        "relx": 0.1,
        "rely": 0.62,
        "relwidth": 0.8,
        "relheight": 0.12
    }
    MID_LAYOUT = {
        "relx": 0.1,
        "rely": 0.9,
        "relwidth": 0.8,
        "relheight": 0.12
    }
    ABOUT_LAYOUT = {
        "relx": 0.9,
        "rely": 0.9,
        "relwidth": 0.8,
        "relheight": 0.12
    }
    IMAGE_LAYOUT = {
        "relx": 0.05,
        "rely": 0.05,
        "relwidth": 0.9,
        "relheight": 0.6
    }
