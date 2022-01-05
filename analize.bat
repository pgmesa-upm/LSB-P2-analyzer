@echo off

@REM Checkeamos que python, pip y virtualenv estan instalados
@REM Ver si python esta instalado
call python --version > nul
if '%errorlevel%' NEQ '0' (
    echo ERROR: Python is not installed, please install it before continuing
    exit /B 1
)
@REM Ver si pip esta instalado
call pip --version > nul
if '%errorlevel%' NEQ '0' (
    echo ERROR: Python package module 'pip' is not installed, please install it before continuing
    exit /B 1
)

@REM  Ver si virtualenv esta instalado y si no lo instalamos
call pip show virtualenv > nul 2>&1
if '%errorlevel%' NEQ '0' (
    echo Instalando virtualenv...
    call pip install virtualenv
)

@REM Crear el virtualenv
set venv_name=venv
if exist %venv_name% (
    cmd /k ".\%venv_name%\Scripts\python.exe analysis.py %*"
) else (
    echo Creando entorno virtual '%venv_name%'...
    call python -m virtualenv %venv_name%
    call .\%venv_name%\Scripts\activate
    echo Instalando dependencias...

    @REM Instalar dependencias y ejecutar el programa
    cmd /k ".\%venv_name%\Scripts\pip.exe install -r requirements.txt & .\%venv_name%\Scripts\python.exe analysis.py %*"
)
pause
