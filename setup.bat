@echo off
echo ========================================
echo World Cup 2026 Intelligence Engine Setup
echo ========================================
echo.

echo [1/4] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed successfully
echo.

echo [2/4] Downloading SpaCy model...
python -m spacy download en_core_web_sm
if %errorlevel% neq 0 (
    echo ERROR: Failed to download SpaCy model
    pause
    exit /b 1
)
echo ✓ SpaCy model downloaded successfully
echo.

echo [3/4] Downloading NLTK data...
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('stopwords'); nltk.download('punkt')"
if %errorlevel% neq 0 (
    echo ERROR: Failed to download NLTK data
    pause
    exit /b 1
)
echo ✓ NLTK data downloaded successfully
echo.

echo [4/4] Verifying installation...
python -c "import streamlit, pandas, plotly, spacy, nltk, bertopic" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Some imports failed, but setup may be complete
) else (
    echo ✓ All packages verified successfully
)
echo.

echo ========================================
echo Setup Complete! 🎉
echo ========================================
echo.
echo To start the dashboard, run:
echo     streamlit run dashboard.py
echo.
echo For detailed usage instructions, see USAGE.md
echo.
pause
