@echo off
SET REQ_FILE=requirements.txt
SET PYTHON_SCRIPT=arduino_communication.py
SET MINICONDA_INSTALLER=%USERPROFILE%\miniconda.exe
SET MINICONDA_PATH=%USERPROFILE%\miniconda3
SET ENV_NAME=Connected-Dice-Rolling

:: Step 1: Check if Miniconda is installed
IF NOT EXIST "%MINICONDA_PATH%" (
    echo Miniconda not found. Installing Miniconda...

    :: Step 2: Download Miniconda installer
    powershell -command "Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile %MINICONDA_INSTALLER%"

    :: Step 3: Install Miniconda silently
    start /B /WAIT %MINICONDA_INSTALLER% /InstallationType=JustMe /AddToPath=0 /RegisterPython=0 /S /D=%MINICONDA_PATH%

    :: Step 4: Clean up the installer
    del %MINICONDA_INSTALLER%

    :: Step 5: Add Miniconda to the system PATH for global use
    echo Adding Miniconda to the system PATH...
    setx Path "%Path%;%UserProfile%\miniconda3\condabin"

) ELSE (
    echo Miniconda already installed.
)

:: Step 6: Initialize Miniconda (if not already initialized)
IF NOT EXIST "%MINICONDA_PATH%\Scripts\conda.exe" (
    echo Initializing Miniconda...
    call "%MINICONDA_PATH%\Scripts\conda.exe" init cmd.exe
)

:: Step 7: Check if the conda environment exists
echo Checking if the environment %ENV_NAME% exists...

:: This will check if the environment exists in the conda list
call "%MINICONDA_PATH%\Scripts\conda.exe" env list | findstr /i "%ENV_NAME%" > nul
IF %ERRORLEVEL% EQU 0 (
    echo Environment %ENV_NAME% found. Activating...
) ELSE (
    echo Environment %ENV_NAME% not found. Creating environment...
    call "%MINICONDA_PATH%\Scripts\conda.exe" create -y -n %ENV_NAME% python=3.9
)

:: Step 8: Activate the environment by using full path for conda
:: We need to source conda from the correct location as we are in a batch script
call "%MINICONDA_PATH%\Scripts\activate.bat" %ENV_NAME%

:: Step 9: Install packages using pip from requirements.txt
echo Installing additional packages from %REQ_FILE% using pip...

IF EXIST "%REQ_FILE%" (
    call pip install -r "%REQ_FILE%"
) ELSE (
    echo %REQ_FILE% not found. Skipping pip install.
)

:: Step 10: Run the Python script
echo Running %PYTHON_SCRIPT%...

:: Run the Python script using `python` from the activated environment
call python "%PYTHON_SCRIPT%"

pause
