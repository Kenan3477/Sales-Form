@echo off
echo ASIS Customer Acquisition Engine - Virtual Environment Setup
echo =============================================================

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing required packages...
pip install -r requirements.txt

echo Testing system...
python simple_validation.py

echo.
echo Virtual environment setup complete!
echo To activate: .venv\Scripts\activate.bat
echo To run campaigns: python customer_acquisition_engine.py --execute-campaign
pause
