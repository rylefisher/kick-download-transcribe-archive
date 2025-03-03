@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo Setting PowerShell execution policy to RemoteSigned...
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

echo Execution policy set to:
powershell -Command "Get-ExecutionPolicy -Scope CurrentUser"

echo Completed. You can now run PowerShell scripts from the venv.
