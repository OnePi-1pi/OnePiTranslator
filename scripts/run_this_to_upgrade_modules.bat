@echo off
title installing
%~dp0\python-3.12.5-embed-amd64\python.exe -m  pip install --upgrade setuptools ttkbootstrap pillow  qrcode  deep_translator regex
%~dp0\python-3.12.5-embed-amd64\python.exe -m pip install --upgrade deep_translator[ai] deep_translator[docx] deep_translator[pdf] 

echo Complete！
pause
exit
