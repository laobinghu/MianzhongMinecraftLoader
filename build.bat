pyinstaller -F -i="./loader.ico" -w main.py

upx -9  --force -v .\dist\ui.exe