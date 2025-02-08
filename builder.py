import os
import subprocess
from config import Config

config = Config()
TempTuple = tuple(config.GetVersion(builder=True))

def nuitka_package(main_file, extra_folder, output_name="main"):
    """
    使用 Nuitka 打包 Tkinter 项目为单文件可执行程序。

    Args:
        main_file (str): 主 Python 文件的路径 (例如: "main.py")
        extra_folder (str): 包含额外资源的文件夹路径 (例如: "assets")
        output_name (str): 输出可执行文件的名称 (不包含扩展名，默认为 "main")
    """

    command = [
        "python",  # 或者使用 python3，取决于你的环境
        "-m",
        "nuitka",
        "--standalone",
        "--onefile",
        "--windows-console-mode=disable",
        r"--windows-icon-from-ico='./loader.ico'",
        "--follow-imports",  # 包含所有依赖项
        "--enable-plugin=tk-inter", # 显式包含tkinter,解决部分打包问题
        "--windows-company-name='绵中方块人服务器管理组'",
        "--windows-product-name='MianzhongMinecraftLoader'",
        "--windows-file-version=2",
        f"--include-data-dir='{extra_folder}={extra_folder}'",  # 包含额外资源文件夹
        f"--output-filename='{output_name}'",  # 设置输出文件名
        main_file,
    ]

    try:
        print("执行 Nuitka 命令:")
        print(" ".join(command))
        subprocess.run(command, check=True)  # check=True 会在命令失败时抛出异常
        print(f"成功打包为单文件可执行程序: {output_name}.exe (位于 dist 文件夹中)")
    except subprocess.CalledProcessError as e:
        print(f"Nuitka 打包失败: {e}")
        print("请检查错误信息，可能需要安装 Nuitka 或解决依赖项问题。")
    except FileNotFoundError:
        print("错误: 找不到 Nuitka。请确保已安装 Nuitka 并将其添加到 PATH 环境变量中。")

if __name__ == "__main__":
    main_file = "main.py"  # 你的主 Python 文件
    extra_folder = "asset"  # 你的额外资源文件夹
    output_name = "MianzhongMinecraftLoader {}".format(config.GetVersion())  # 你想要的可执行文件名称
    print("当前打包版本",TempTuple)
    # 检查文件和文件夹是否存在
    if not os.path.exists(main_file):
        print(f"错误: 找不到主文件: {main_file}")
    elif not os.path.exists(extra_folder):
        print(f"错误: 找不到额外资源文件夹: {extra_folder}")
    else:
        nuitka_package(main_file, extra_folder, output_name)
