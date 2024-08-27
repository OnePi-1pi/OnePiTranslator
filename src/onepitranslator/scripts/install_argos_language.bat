@echo off


setlocal

set "user_dir=%USERPROFILE%"


set "target_dir=%user_dir%\.local\share\argos-translate\packages"


if not exist "%target_dir%" mkdir "%target_dir%"


"%~dp0\7za.exe" x "packages.7z" -o"%target_dir%"

endlocal

