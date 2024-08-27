@echo off
title installing
%~dp0\python-3.12.5-embed-amd64\python.exe -m  pip install --upgrade -r %~dp0\requirements.txt
echo Complete！
pause
exit
