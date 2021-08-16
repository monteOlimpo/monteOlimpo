@echo off
PUSHD %~dp0
echo instalando python
start /wait python-3.8.exe /s
echo instalando dependencias
py -m pip install flask flask-cors selenium
cd ..
ROBOCOPY ./csg-listener C:/csg-listener > nul
cd csg-listener
copy /y load.pyw load-file.pyw
move load-file.pyw "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
