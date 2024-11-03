@echo off
cd %~dp0
setlocal

set PY="py"

git pull
%PY% -m pip install -r requirements.lock

set /p TOKEN=<..\CMTK.txt
copy /Y ..\config.json .\config\
%PY% CommandLab.py

endlocal
pause