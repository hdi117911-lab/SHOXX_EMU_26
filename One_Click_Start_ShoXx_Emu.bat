@echo off
title ShoXx_Emu // 100%% Portable Stealth Smartphone Emulator (Android 15/16/17 + Play Store + Root)
set "SHOXX_ROOT=%~dp0"
if "%SHOXX_ROOT:~-1%"=="\" set "SHOXX_ROOT=%SHOXX_ROOT:~0,-1%"
cd /d "%SHOXX_ROOT%"

REM Strictly isolate all Android SDK, AVD, ADB, Temp and User paths inside the portable folder
set "ANDROID_SDK_ROOT=%SHOXX_ROOT%\sdk"
set "ANDROID_HOME=%SHOXX_ROOT%\sdk"
set "ANDROID_SDK_HOME=%SHOXX_ROOT%\avd_data"
set "ANDROID_PREFS_ROOT=%SHOXX_ROOT%\avd_data"
set "ANDROID_AVD_HOME=%SHOXX_ROOT%\avd_data\.android\avd"
set "ANDROID_USER_HOME=%SHOXX_ROOT%\avd_data\.android"
set "ANDROID_EMULATOR_HOME=%SHOXX_ROOT%\avd_data\.android"
set "ADB_VENDOR_KEYS=%SHOXX_ROOT%\avd_data\.android"
set "HOME=%SHOXX_ROOT%\avd_data"
set "USERPROFILE=%SHOXX_ROOT%\avd_data"
set "LOCALAPPDATA=%SHOXX_ROOT%\avd_data"
set "APPDATA=%SHOXX_ROOT%\avd_data"
set "TEMP=%SHOXX_ROOT%\_cache\temp"
set "TMP=%SHOXX_ROOT%\_cache\temp"
if not exist "%TEMP%" mkdir "%TEMP%"
if not exist "%SHOXX_ROOT%\downloads" mkdir "%SHOXX_ROOT%\downloads"

set "PATH=%SHOXX_ROOT%\python_portable;%SHOXX_ROOT%\sdk\emulator;%SHOXX_ROOT%\sdk\platform-tools;%PATH%"

if exist "%SHOXX_ROOT%\python_portable\pythonw.exe" (
    start "" "%SHOXX_ROOT%\python_portable\pythonw.exe" "%SHOXX_ROOT%\ShoXx_Emu.py" %*
) else (
    start "" pythonw "%SHOXX_ROOT%\ShoXx_Emu.py" %*
)
exit /b 0
