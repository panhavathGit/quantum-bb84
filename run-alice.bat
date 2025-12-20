@echo off
echo Starting Alice's BB84 Terminal
echo.
echo Installing requirements...
pip install -r requirements-streamlit.txt
echo.
echo Starting Alice's interface on port 8501...
echo Open browser to: http://localhost:8501
echo.
streamlit run alice-app.py --server.port 8501
pause
