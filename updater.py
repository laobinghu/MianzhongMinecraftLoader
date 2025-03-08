from requests import request
from json import loads
from config import Config

version = Config().GetVersion(updater=False)

url = "https://git.mzmc.top/api/v1/repos/laobinghu/MianzhongMinecraftLoader/releases/latest"

payload={}
headers = {"User-Agent":r"Mozilla/5.0 (compatible; MzmcOS; +https://mzmc.top) MzmcOS/Loader"}

response = loads(request("GET", url, headers=headers, data=payload).text)
remote_version = response["name"]
link = response["assets"][0]["browser_download_url"]
body = response["body"]
def check_update():
    result = not remote_version != version

    return result,remote_version,link,body

if __name__ == "__main__":
    if check_update()[0]:
        print("已为最新")
    else:
        print(f"发现更新:{remote_version}\n链接:{link}")

