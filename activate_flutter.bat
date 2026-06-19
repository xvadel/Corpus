@echo off
REM Flutter Environment Activation Script (CMD version)
echo ========================================
echo   Activating Flutter Environment...
echo ========================================

call conda activate flutter_env

set JAVA_HOME=C:\Users\LOQ\miniconda3\envs\flutter_env\Library
set ANDROID_HOME=d:\Lantest\android-sdk
set ANDROID_SDK_ROOT=d:\Lantest\android-sdk
set PATH=d:\Lantest\flutter-sdk\bin;d:\Lantest\android-sdk\cmdline-tools\latest\bin;d:\Lantest\android-sdk\platform-tools;C:\Users\LOQ\miniconda3\envs\flutter_env\Library\bin;%PATH%

echo.
echo [OK] Conda env: flutter_env
echo [OK] JAVA_HOME: %JAVA_HOME%
echo [OK] ANDROID_HOME: %ANDROID_HOME%
echo [OK] Flutter SDK: d:\Lantest\flutter-sdk
echo.
echo Ready! Run 'flutter doctor' to verify.
echo ========================================
