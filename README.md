# Create virtual environment
python -m venv venv

# For Mac/Linux:
source venv/bin/activate

# For Windows:
venv\Scripts\activate

# Install dependencies
pip install flask flask-cor

# To run 
python quantum_encryption.py
python quantum-keygen.py


# bb84 run python server
# run in bash

python quantum_encryption.py

# use to run alice side 
 streamlit run alice-app.py --server.port 8501

 # use to run bob side 
 streamlit run bob-app.py --server.port 8502
