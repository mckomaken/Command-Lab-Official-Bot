@echo off
cd %~dp0

set PY="python"

if exist ".\_StartBot" (
    mkdir tmp
    copy .\_StartBot\tmp\bump_data.json .\tmp\
    rd /S /Q .\_StartBot
)

git clone git@github.com:Syunngiku0402/Command-Lab-Official-Bot _StartBot
cd .\_StartBot
rd /S /Q .git


%PY% -m pip install -r requirements.txt
copy /Y ..\config.json .\config\config.json
copy /Y ..\CMTK.txt .\CMTK.txt
mkdir tmp

copy ..\tmp\bump_data.json .\tmp\
rd /S /Q ..\tmp

%PY% CommandLab.py
exit