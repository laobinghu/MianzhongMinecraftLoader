from requests import request
from json import loads
from config import Config

version = Config().GetVersion(updater=True)

url = "https://mc.boen.fun/api/loader/update"

payload={}
headers = {"User-Agent":r"Mozilla/5.0 (compatible; MzmcOS; +https://mc.boen.fun) MzmcOS/Loader"}

response = loads(request("GET", url, headers=headers, data=payload).text)

