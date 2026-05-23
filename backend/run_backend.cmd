@echo off
setlocal
set ROOT=%~dp0..

if exist "%ROOT%\.venv\Scripts\python.exe" (
  set PY=%ROOT%\.venv\Scripts\python.exe
) else if exist "%~dp0venv\Scripts\python.exe" (
  set PY=%~dp0venv\Scripts\python.exe
) else (
  echo No venv found. Run setup_backend.cmd first.
  exit /b 1
)

cd /d "%~dp0"
%PY% -m uvicorn app.main:app --reload

endlocal
