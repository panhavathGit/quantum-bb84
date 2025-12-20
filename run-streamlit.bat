@echo off
echo Starting BB84 Quantum Key Generator (Streamlit)
echo.
echo Installing required packages...
pip install -r requirements-streamlit.txt
echo.
echo Starting Streamlit app...
echo Open browser to: http://localhost:8501
echo.
streamlit run streamlit-keygen.py
pause
