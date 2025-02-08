from threading import Thread
from ui import MinecraftLoader
from tkinter import Tk
from log import Logger

logger = Logger(__name__)
logger.info("程序启动")
root = Tk()
loader = MinecraftLoader(root)
Thread(target=loader.main_loop).start()
root.mainloop()
logger.info("程序退出")

