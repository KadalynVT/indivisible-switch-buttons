. .\venv\Scripts\Activate.ps1
pyinstaller --noconfirm --onedir --console --add-data "D:\dev\indivisible\indivisible_switch_buttons\nvcompress.exe;." --add-data "D:\dev\indivisible\indivisible_switch_buttons\nvtt.dll;." --add-data "D:\dev\indivisible\indivisible_switch_buttons\venv\Lib\site-packages\dividedpkg\key.dat;dividedpkg"  "D:\dev\indivisible\indivisible_switch_buttons\main.py"
