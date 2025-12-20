@echo off
echo Starting BB84 Quantum Key Exchange Demo
echo.
echo Installing requirements...
pip install -r requirements-streamlit.txt
echo.
echo Starting both Alice and Bob interfaces...
echo.
echo Alice will be at: http://localhost:8501
echo Bob will be at: http://localhost:8502
echo.

start "Alice Terminal" cmd /k "streamlit run alice-app.py --server.port 8501"
timeout /t 3
start "Bob Terminal" cmd /k "streamlit run bob-app.py --server.port 8502"

echo.
echo Both terminals started!
echo Press any key to close this window...
pause > nul
