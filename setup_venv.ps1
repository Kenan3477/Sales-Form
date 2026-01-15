# ASIS Customer Acquisition Engine - Virtual Environment Setup
# ===========================================================

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt

# Test system
python simple_validation.py

Write-Host "Virtual environment setup complete!" -ForegroundColor Green
Write-Host "To run campaigns: python customer_acquisition_engine.py --execute-campaign" -ForegroundColor Yellow
