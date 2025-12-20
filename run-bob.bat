@echo off
echo Starting Bob's BB84 Terminal
echo.
echo Installing requirements...
pip install -r requirements-streamlit.txt
echo.
echo Starting Bob's interface on port 8502...
echo Open browser to: http://localhost:8502
echo.
streamlit run bob-app.py --server.port 8502
pause
