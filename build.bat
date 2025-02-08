pyinstaller -F -i="./loader.ico" --add-data "asset/;." -w main.py
upx -9  --force -v .\dist\ui.exe