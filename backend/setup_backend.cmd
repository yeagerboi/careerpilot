@echo off
setlocal
set ROOT=%~dp0..

if not exist "%ROOT%\.venv\Scripts\python.exe" (
  echo Creating venv at %ROOT%\.venv
  python -m venv "%ROOT%\.venv"
)

call "%ROOT%\.venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r "%~dp0requirements.txt"

endlocal
