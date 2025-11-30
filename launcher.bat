@echo off
setlocal

set "BASE=%~dp0"
set "PY=%BASE%python\pythonw.exe"
set "MAIN=%BASE%launcher.py"

start "" "%PY%" "%MAIN%"
exit