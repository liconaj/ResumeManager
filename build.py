import os
import sys

CWD = os.getcwd().replace("\\", "/")
PYTHON_EXE_PATH = "C:/Users/Josue/Documents/Proyectos/ResumeManager/.qtcreator/Python_3_10_11venv/Scripts/python.exe"

metadata = dict()
fhandler = open("metadata.txt", "r", encoding="utf-8")
for line in fhandler:
    item = line.strip().split("=")
    key = item[0].strip()
    value = item[1].strip()
    metadata[key] = value
fhandler.close()

if os.path.exists("dist/ResumeManager"):
    print("Removing old directory dist/ResumeManager")
    os.system("rmdir /s /q dist\\ResumeManager")

command = '{} -m nuitka '.format(PYTHON_EXE_PATH)
command += '--standalone '
command += '--windows-console-mode=attach '
command += '--output-dir="{}/dist" '.format(CWD)
command += '--remove-output '
command += '--output-filename="{}" '.format(metadata["filename"])
command += '--enable-plugin=pyside6 '
command += '--noinclude-setuptools-mode=nofollow '
command += '--mingw64 --jobs=16 '
command += '--force-stderr-spec=logs.out.txt '
command += '--force-stdout-spec=logs.out.txt '
command += '--product-version={} '.format(metadata["version"])
command += '--company-name="{}" '.format(metadata["company"])
command += '--product-name="{}" '.format(metadata["name"])
command += '--windows-icon-from-ico="{}" '.format(metadata["icon-windows"])
command += '--file-description="{}" '.format(metadata["description"])
command += '--copyright="{}" '.format(metadata["copyright"])
command += '--include-data-files=credentials.json=credentials.json '
command += '--include-data-files=config.txt=config.txt '
command += '--include-data-dir=ui=ui '
command += '--include-data-dir=data=data '
command += '--main="{}" &'.format("main.py")
command += 'move "dist/main.dist" "dist/ResumeManager"'

os.system(f"cmd /c {command}")

