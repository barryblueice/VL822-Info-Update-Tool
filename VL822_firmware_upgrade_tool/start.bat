@ECHO off
echo [92mVL822[0m [96mFirmware Upgrade Tool[0m, [95mmodified by barryblueice[0m, [90m2025.[0m
echo.
echo [91mDuring the Firmware Update Process, DO NOT DISCONNECT THE AC ADAPTER!!![0m
echo.
timeout /t 3 >nul
HUBIspTool.exe
echo [92mUpgrading Process Complete! Press any key to Exit...
pause