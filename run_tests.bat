@echo off
echo ============================================
echo Financial Bot Discord - Test Runner
echo ============================================
echo.

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/3] Running all tests...
echo.
python -m pytest tests/ -v --tb=short

echo.
echo [3/3] Test Summary:
echo ============================================
echo Tests completed!
echo ============================================
pause
