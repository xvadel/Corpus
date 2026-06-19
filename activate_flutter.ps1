# Flutter Environment Activation Script
# Usage: . .\activate_flutter.ps1
# (Note: use dot-sourcing with the leading dot+space to apply to current session)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Activating Flutter Environment...     " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Activate conda environment
conda activate flutter_env

# Set JAVA_HOME to conda's JDK 17
$env:JAVA_HOME = "C:\Users\LOQ\miniconda3\envs\flutter_env\Library"

# Set Android SDK
$env:ANDROID_HOME = "d:\Lantest\android-sdk"
$env:ANDROID_SDK_ROOT = "d:\Lantest\android-sdk"

# Add Flutter, Android tools, and Java to PATH
$env:Path = "d:\Lantest\flutter-sdk\bin;d:\Lantest\android-sdk\cmdline-tools\latest\bin;d:\Lantest\android-sdk\platform-tools;C:\Users\LOQ\miniconda3\envs\flutter_env\Library\bin;" + $env:Path

Write-Host ""
Write-Host "[OK] Conda env: flutter_env" -ForegroundColor Green
Write-Host "[OK] JAVA_HOME: $env:JAVA_HOME" -ForegroundColor Green
Write-Host "[OK] ANDROID_HOME: $env:ANDROID_HOME" -ForegroundColor Green
Write-Host "[OK] Flutter SDK: d:\Lantest\flutter-sdk" -ForegroundColor Green
Write-Host ""
Write-Host "Ready! Run 'flutter doctor' to verify." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
