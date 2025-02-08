from threading import Thread
from ui import MinecraftLoader
from tkinter import Tk

root = Tk()
loader = MinecraftLoader(root)
Thread(target=loader.main_loop).start()
root.mainloop()
