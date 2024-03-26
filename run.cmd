@echo off
cd %~dp0

set PY="python"

if exist ".\_StartBot" (
    rd /S /Q .\_StartBot
)

git clone git@github.com:Syunngiku0402/Command-Lab-Official-Bot _StartBot
cd .\_StartBot
rd /S /Q .git

%PY% -m pip install -r requirements.txt
copy /Y ..\config.json .\config\config.json
copy /Y ..\CMTK.txt .\CMTK.txt
mkdir tmp

%PY% CommandLab.py
exit