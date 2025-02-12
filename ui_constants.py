class UIConstants:
    """UI配置常量类"""
    # 窗口设置
    WINDOW_TITLE = "Mianzhong Minecraft Loader"
    WINDOW_SIZE = (500, 320)
    GEOMETRY_FORMAT = "%dx%d+%d+%d"

    # 颜色配置
    BACKGROUND_COLOR = "#FFFFFF"
    TEXT_COLOR = "#2C3E50"
    PROGRESS_COLOR = "#3498DB"
    PROGRESS_BG_COLOR = "#D6DBDF"

    # 字体配置
    FONT_LABEL = ("微软雅黑", 10)
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
        "rely": 0.85,
        "relwidth": 0.9,
        "relheight": 0.08
    }
    LABEL_LAYOUT = {
        "relx": 0.1,
        "rely": 0.68,
        "relwidth": 0.8,
        "relheight": 0.12
    }
    IMAGE_LAYOUT = {
        "relx": 0.05,
        "rely": 0.05,
        "relwidth": 0.9,
        "relheight": 0.6
    }
