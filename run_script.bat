@echo off
:: Check if numpy is installed
python -c "import numpy" 2>nul
if %errorlevel% neq 0 (
    echo Numpy is not installed. Installing numpy...
    pip install numpy
)

:: Run the Python script
python main1.py
pause--