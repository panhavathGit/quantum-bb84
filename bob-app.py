"""
BB84 Quantum Key Generator - Bob's Interface
Dedicated interface for Bob (Receiver) in the BB84 protocol

HOW TO RUN:
1. Install requirements: pip install -r requirements-streamlit.txt
2. Run Bob's app: streamlit run bob-app.py --server.port 8502
3. Bob: http://localhost:8502
4. Alice: http://localhost:8501 (run alice-app.py)
"""

import streamlit as st
import random
import time
import pandas as pd
import plotly.graph_objects as go
import json
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="BB84 - Bob (Receiver)",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Shared state file path
SHARED_STATE_FILE = Path("shared_bb84_state.json")

# Custom CSS for Bob's theme
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #00bfff;
    font-size: 3em;
    font-weight: bold;
    text-shadow: 0 0 30px #00bfff;
    margin-bottom: 30px;
    background: linear-gradient(135deg, #00bfff, #1e90ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.bob-panel {
    background: linear-gradient(135deg, #0d1a2e, #1b2d69);
    border: 3px solid #00bfff;
    border-radius: 20px;
    padding: 30px;
    margin: 15px;
    box-shadow: 0 0 40px rgba(0, 191, 255, 0.3);
}
.bob-metric {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #00bfff, #1e90ff);
    color: white;
    border-radius: 15px;
    margin: 10px;
    font-weight: bold;
    box-shadow: 0 5px 15px rgba(0, 191, 255, 0.4);
}
.status-ready { color: #00ff88; }
.status-waiting { color: #ffaa00; }
.status-error { color: #ff4444; }
</style>
""", unsafe_allow_html=True)

def load_shared_state():
    """Load shared state from file"""
    if SHARED_STATE_FILE.exists():
        try:
            with open(SHARED_STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        "alice_bits": [],
        "alice_bases": [],
        "alice_message": "",
        "bob_bases": [],
        "bob_results": [],
        "bob_message": "",
        "phase": "greeting",
        "sifted_bits": [],
        "matching_indices": [],
        "error_rate": 0.0,
        "final_key": "",
        "eve_present": False,
        "alice_ready": False,
        "bob_ready": False
    }

def save_shared_state(state):
    """Save shared state to file"""
    try:
        with open(SHARED_STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        st.error(f"Error saving state: {e}")

def simulate_measurement(alice_bases, alice_bits, method="random", eve_present=False):
    """Simulate Bob's measurements with better data handling"""
    bob_bases = []
    bob_results = []
    
    # Ensure clean input data
    transmitted_bits = [int(b) if b in [0, 1, '0', '1'] else 0 for b in alice_bits]
    
    if eve_present:
        for i in range(len(transmitted_bits)):
            if random.random() < 0.6:  # 60% interception
                if random.random() < 0.5:  # Wrong basis 50% of time
                    transmitted_bits[i] = random.randint(0, 1)
    
    for i in range(len(alice_bases)):
        # Bob chooses measurement basis
        if method == "random":
            basis = random.randint(0, 1)
        else:
            basis = random.randint(0, 1)  # Simplified
        
        bob_bases.append(basis)
        
        # Measurement result - ensure integer
        if alice_bases[i] == basis:
            result = int(transmitted_bits[i])
        else:
            result = random.randint(0, 1)
        
        bob_results.append(result)
    
    return bob_bases, bob_results

def main():
    # Header
    st.markdown('<h1 class="main-header">🔬 BOB - Quantum Receiver</h1>', 
                unsafe_allow_html=True)
    
    # Load current state
    shared_state = load_shared_state()
    
    # Sidebar controls
    st.sidebar.title("🔬 Bob's Controls")
    st.sidebar.markdown("**Role:** Quantum bit receiver")
    
    # Configuration
    st.sidebar.subheader("Measurement Settings")
    measurement_method = st.sidebar.selectbox("Measurement Strategy", ["random", "manual"])
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📨 Communication with Alice")
        
        # Greeting Phase
        if shared_state["phase"] == "greeting":
            st.info("👋 **Waiting for Alice's greeting...**")
            
        elif shared_state["phase"] == "waiting_bob_response":
            if shared_state.get("alice_message"):
                st.success(f"📨 **Alice says:** {shared_state['alice_message']}")
                
                bob_response = st.text_input("Your response:", 
                                           value="Hello Alice! I'm ready for the quantum protocol!")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Confirm Ready"):
                        shared_state["bob_message"] = bob_response
                        shared_state["bob_ready"] = True
                        shared_state["phase"] = "preparation"
                        save_shared_state(shared_state)
                        st.success("✅ Confirmed! Waiting for Alice to start protocol...")
                        st.rerun()
                
                with col_b:
                    if st.button("❌ Not Ready"):
                        shared_state["bob_ready"] = False
                        save_shared_state(shared_state)
                        st.warning("⏸️ Told Alice you're not ready")
        
        # Protocol phases
        elif shared_state["phase"] == "preparation":
            st.info("⏳ **Waiting for Alice to prepare qubits...**")
        
        elif shared_state["phase"] == "transmission":
            st.info("📡 **Alice is transmitting qubits...**")
        
        elif shared_state["phase"] == "waiting_bob_measurement":
            st.success("🔬 **Step 3:** Measure received qubits")
            st.warning(f"📦 **Received {len(shared_state['alice_bits'])} qubits from Alice**")
            
            if st.button("🔍 Start Measurements"):
                with st.spinner("Measuring qubits..."):
                    bob_bases, bob_results = simulate_measurement(
                        shared_state["alice_bases"],
                        shared_state["alice_bits"],
                        measurement_method,
                        shared_state.get("eve_present", False)
                    )
                    shared_state["bob_bases"] = bob_bases
                    shared_state["bob_results"] = bob_results
                    shared_state["phase"] = "sifting"
                    save_shared_state(shared_state)
                st.success(f"✅ Measured all {len(bob_results)} qubits!")
                st.rerun()
        
        elif shared_state["phase"] == "sifting":
            st.info("🔍 **Waiting for Alice to start sifting...**")
            
            if shared_state.get("sifted_bits"):
                st.success("✅ Sifting completed by Alice!")
        
        elif shared_state["phase"] == "error_check":
            st.info("⚠️ **Alice is checking for errors...**")
        
        elif shared_state["phase"] == "key_generation":
            st.info("🔑 **Alice is generating the final key...**")
        
        elif shared_state["phase"] == "complete":
            st.success("🎉 **Protocol Complete!**")
            st.balloons()
    
    with col2:
        st.markdown("### 📊 Bob's Data")
        
        # Current status
        phase_status = {
            "greeting": "👋 Waiting for Alice",
            "waiting_bob_response": "📨 Respond to Alice",
            "preparation": "⏳ Alice preparing",
            "transmission": "📡 Receiving qubits",
            "waiting_bob_measurement": "🔬 Ready to measure",
            "sifting": "🔍 Sifting in progress",
            "error_check": "⚠️ Error checking",
            "key_generation": "🔑 Key generation",
            "complete": "✅ Complete"
        }
        
        st.info(f"**Status:** {phase_status.get(shared_state['phase'], 'Unknown')}")
        
        # Bob's measurement data
        if shared_state.get("bob_results"):
            st.subheader("🔬 Measurements")
            
            # Show sample data
            sample_size = min(10, len(shared_state["bob_results"]))
            df_bob = pd.DataFrame({
                'Q#': range(1, sample_size + 1),
                'Basis': ['+' if b == 0 else '×' for b in shared_state["bob_bases"][:sample_size]],
                'Result': shared_state["bob_results"][:sample_size],
                'Match': ['✓' if shared_state["alice_bases"][i] == shared_state["bob_bases"][i] 
                         else '✗' for i in range(sample_size)]
            })
            st.dataframe(df_bob, use_container_width=True)
            
            if len(shared_state["bob_results"]) > 10:
                st.caption(f"Showing 10 of {len(shared_state['bob_results'])} measurements")
        
        # Eavesdropper indicator
        if shared_state.get("eve_present"):
            st.warning("👁️ **Eavesdropper Active**")
            st.caption("Eve is intercepting qubits!")
    
    # Visualization
    if shared_state.get("bob_results"):
        st.markdown("### 📈 Bob's Measurement Visualization")
        
        # Create comparison visualization
        display_limit = min(50, len(shared_state["bob_results"]))
        
        fig = go.Figure()
        
        # Bob's bases
        fig.add_trace(go.Scatter(
            x=list(range(1, display_limit + 1)),
            y=shared_state["bob_bases"][:display_limit],
            mode='markers+lines',
            name='Bob Basis',
            marker=dict(color='lightblue', size=8),
            line=dict(color='blue', width=2)
        ))
        
        # Alice's bases (for comparison)
        if shared_state.get("alice_bases"):
            fig.add_trace(go.Scatter(
                x=list(range(1, display_limit + 1)),
                y=shared_state["alice_bases"][:display_limit],
                mode='markers+lines',
                name='Alice Basis',
                marker=dict(color='pink', size=6),
                line=dict(color='red', width=2, dash='dash')
            ))
        
        # Bob's results
        fig.add_trace(go.Scatter(
            x=list(range(1, display_limit + 1)),
            y=shared_state["bob_results"][:display_limit],
            mode='markers+lines',
            name='Measurement Result',
            marker=dict(color='cyan', size=8),
            line=dict(color='darkblue', width=2),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Bob's Measurements vs Alice's Preparation",
            xaxis_title="Qubit Number",
            yaxis=dict(title="Basis (0=+, 1=×)", side="left"),
            yaxis2=dict(title="Bit Value", overlaying="y", side="right"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Matching statistics
        if shared_state.get("alice_bases"):
            matches = sum(1 for i in range(len(shared_state["bob_bases"])) 
                         if shared_state["alice_bases"][i] == shared_state["bob_bases"][i])
            match_rate = matches / len(shared_state["bob_bases"]) * 100
            
            st.metric("Basis Match Rate", f"{match_rate:.1f}%")
    
    # Final key display
    if shared_state.get("final_key"):
        st.markdown("### 🔑 Shared Quantum Key")
        
        st.success("✅ **Quantum key successfully established!**")
        
        # Key display
        st.code(shared_state["final_key"], language="text")
        
        # Chat Demo Link
        st.markdown("---")
        st.markdown("### 🚀 **Bob: Ready for Quantum Chat!**")
        
        # Create clickable link with Bob's styling
        st.markdown("""
        <div style='text-align: center; margin: 20px 0;'>
            <a href="http://localhost:3000" target="_blank" style='
                display: inline-block;
                background: linear-gradient(45deg, #00bfff, #1e90ff);
                color: #fff;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 18px;
                text-transform: uppercase;
                letter-spacing: 2px;
                box-shadow: 0 0 20px rgba(0, 191, 255, 0.5);
                transition: all 0.3s ease;
            '>
                🔬 BOB: JOIN QUANTUM CHAT
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Security assessment
        error_rate = shared_state.get("error_rate", 0)
        if error_rate > 0.15:
            st.error("🚨 **HIGH ERROR RATE!** Possible eavesdropper detected!")
            if shared_state.get("eve_present"):
                st.success("✅ BB84 protocol correctly detected Eve!")
        elif error_rate > 0.05:
            st.warning("⚠️ **Moderate error rate.** Channel security questionable.")
        else:
            st.success("🔒 **Low error rate.** Secure quantum channel established!")
        
        # Instructions
        st.info("""
        **🎯 Bob's Next Steps:**
        1. Click "Bob: Join Quantum Chat" above
        2. Enter username as "Bob"
        3. Paste the shared quantum key
        4. Connect with Alice who has the same key
        5. Decrypt Alice's encrypted messages!
        """)
    
    # Auto-refresh for real-time updates
    if shared_state["phase"] in ["greeting", "preparation", "transmission", "sifting", "error_check", "key_generation"]:
        time.sleep(2)
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #00bfff;'>
    <p><strong>🔬 Bob's Quantum Terminal</strong></p>
    <p>Alice connected at: <code>http://localhost:8501</code></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
