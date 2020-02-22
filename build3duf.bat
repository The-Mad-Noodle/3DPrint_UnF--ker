echo Packaging 3D Print UnFucker
cd venv/Scripts & activate.bat & cd .. & cd .. & pyinstaller --onefile -w --icon=img/unf_SFW.ico main.py & del main.spec & rd /s /q "build" & cd dist & MOVE main.exe ../main.exe & cd .. & rd dist & echo Packaging complete & rename main.exe "3D PUF.exe" & PAUSE
