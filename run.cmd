@echo off
cd %~dp0
setlocal

set PY="py"

git pull
%PY% -m pip install -r requirements.txt

set /p TOKEN=<..\CMTK.txt
%PY% CommandLab.py

endlocal
pause