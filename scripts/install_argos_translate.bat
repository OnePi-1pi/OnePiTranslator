@echo off
title installing offlinetranslate - argostranslate
echo must use administrator privileges to install offline translation, otherwise it will make spacy or torch unavailable after installation
setlocal
set uac=~uac_permission_tmp_%random%
md "%SystemRoot%\system32\%uac%" 2>nul
if %errorlevel%==0 ( rd "%SystemRoot%\system32\%uac%" >nul 2>nul ) else (
    echo set uac = CreateObject^("Shell.Application"^)>"%temp%\%uac%.vbs"
    echo uac.ShellExecute "%~s0","","","runas",1 >>"%temp%\%uac%.vbs"
    echo WScript.Quit >>"%temp%\%uac%.vbs"
    "%temp%\%uac%.vbs" /f
    del /f /q "%temp%\%uac%.vbs" & exit )
endlocal
echo ok!

echo  
%~dp0\python-3.12.5-embed-amd64\python.exe -m pip install  --upgrade argostranslate 

%~dp0\python-3.12.5-embed-amd64\python.exe -m pip install %~dp0\whl\xxx_sent_ud_sm-3.7.0-py3-none-any.whl
echo   

echo complete,if you want to use CUDA ,you also need to install  nvidia driver and cuda Version compliant  with nvtorch
echo https://developer.nvidia.com/cuda-downloads
echo https://developer.nvidia.com/drive/downloads
pause
exit
