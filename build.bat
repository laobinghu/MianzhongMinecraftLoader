pyinstaller -F -i="./loader.ico" -w ui.py
upx -9  --force -v .\dist\ui.exe