"""
BB84 Quantum Key Generator - Alice's Interface
Dedicated interface for Alice (Sender) in the BB84 protocol

HOW TO RUN:
1. Install requirements: pip install -r requirements-streamlit.txt
2. Run Alice's app: streamlit run alice-app.py --server.port 8501
3. Run Bob's app in separate terminal: streamlit run bob-app.py --server.port 8502
4. Run Huot's app: streamlit run huot-app.py --server.port 8503
5. Alice: http://localhost:8501
6. Bob: http://localhost:8502
7. Huot: http://localhost:8503
"""

import streamlit as st
import random
import hashlib
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import os
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="BB84 - Alice (Sender)",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Shared state file path
SHARED_STATE_FILE = Path("shared_bb84_state.json")

# Custom CSS for Alice's theme
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #ff69b4;
    font-size: 3em;
    font-weight: bold;
    text-shadow: 0 0 30px #ff69b4;
    margin-bottom: 30px;
    background: linear-gradient(135deg, #ff69b4, #ff1493);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.alice-panel {
    background: linear-gradient(135deg, #2d1b3d, #4a2f5a);
    border: 3px solid #ff69b4;
    border-radius: 20px;
    padding: 30px;
    margin: 15px;
    box-shadow: 0 0 40px rgba(255, 105, 180, 0.3);
}
.alice-metric {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #ff69b4, #ff1493);
    color: white;
    border-radius: 15px;
    margin: 10px;
    font-weight: bold;
    box-shadow: 0 5px 15px rgba(255, 105, 180, 0.4);
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
        "alice_selected_partner": "bob",  # Default partner
        "bob_bases": [],
        "bob_results": [],
        "bob_message": "",
        "huot_bases": [],
        "huot_results": [],
        "huot_message": "",
        "phase": "greeting",
        "sifted_bits": [],
        "matching_indices": [],
        "error_rate": 0.0,
        "final_key": "",
        "eve_present": False,
        "alice_ready": False,
        "bob_ready": False,
        "huot_ready": False
    }

def save_shared_state(state):
    """Save shared state to file"""
    try:
        with open(SHARED_STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        st.error(f"Error saving state: {e}")

def generate_qubits(num_qubits, method="random"):
    """Generate Alice's qubits"""
    bits = []
    bases = []
    
    for i in range(num_qubits):
        if method == "random":
            bits.append(random.randint(0, 1))
            bases.append(random.randint(0, 1))
        else:
            # Manual mode - could be expanded for interactive selection
            bits.append(random.randint(0, 1))
            bases.append(random.randint(0, 1))
    
    return bits, bases

def perform_sifting(alice_bits, alice_bases, partner_bases, partner_results):
    """Perform basis sifting"""
    sifted_bits = []
    matching_indices = []
    
    # Ensure all arrays have the same length
    min_length = min(len(alice_bits), len(alice_bases), len(partner_bases), len(partner_results))
    
    for i in range(min_length):
        if alice_bases[i] == partner_bases[i]:
            sifted_bits.append(int(partner_results[i]))  # Ensure integer
            matching_indices.append(i)
    
    return sifted_bits, matching_indices

def error_checking(alice_bits, sifted_bits, matching_indices, has_eavesdropper=False):
    """Perform error checking"""
    total_bits = len(sifted_bits)
    if total_bits == 0:
        return 0.0, 0, []
    
    errors = 0
    
    for idx in range(total_bits):
        if idx < len(matching_indices) and matching_indices[idx] < len(alice_bits):
            alice_bit = alice_bits[matching_indices[idx]]
            partner_bit = sifted_bits[idx]
            if alice_bit != partner_bit:
                errors += 1
    
    if has_eavesdropper:
        additional_errors = random.randint(1, max(1, total_bits // 15))
        errors += additional_errors
    
    error_rate = errors / total_bits if total_bits > 0 else 0
    
    # Remove bits used for error checking
    sacrifice_count = min(errors + 1, max(1, len(sifted_bits) // 8))
    remaining_bits = sifted_bits[:-sacrifice_count] if sacrifice_count > 0 and sacrifice_count < len(sifted_bits) else sifted_bits
    
    return error_rate, errors, remaining_bits

def generate_final_key(sifted_bits):
    """Generate final key"""
    if not sifted_bits or len(sifted_bits) < 4:
        return None
    
    try:
        bit_string = ''.join(str(int(b)) for b in sifted_bits)
        while len(bit_string) % 8 != 0:
            bit_string += '0'
        
        byte_data = bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))
        final_key = hashlib.sha256(byte_data).hexdigest()
        
        return final_key
    except (ValueError, TypeError, OverflowError):
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🎭 ALICE - Quantum Sender</h1>', 
                unsafe_allow_html=True)
    
    # Load current state
    shared_state = load_shared_state()
    
    # Sidebar controls
    st.sidebar.title("🎭 Alice's Controls")
    st.sidebar.markdown("**Role:** Quantum bit sender")
    
    # Partner Selection
    st.sidebar.subheader("🎯 Enter Quantum Partner")
    current_partner = shared_state.get("alice_selected_partner", "bob")
    
    selected_partner = st.sidebar.text_input(
        "Type your quantum partner's name:", 
        value=current_partner,
        placeholder="Enter partner name (e.g., Bob, Huot, Carol, Dave...)",
        help="Enter the name of who you want to exchange quantum keys with"
    ).lower().strip()
    
    # Update partner selection
    if selected_partner and selected_partner != shared_state.get("alice_selected_partner", "bob"):
        shared_state["alice_selected_partner"] = selected_partner
        # Reset protocol when changing partners
        shared_state["phase"] = "greeting"
        shared_state["alice_ready"] = False
        # Reset all possible partner states
        shared_state["bob_ready"] = False
        shared_state["huot_ready"] = False
        if f"{selected_partner}_ready" in shared_state:
            shared_state[f"{selected_partner}_ready"] = False
        save_shared_state(shared_state)
        st.sidebar.success(f"✅ Partner changed to {selected_partner.title()}!")
        st.rerun()
    
    # Show partner status if partner name is provided
    if selected_partner:
        partner_ready_key = f"{selected_partner}_ready"
        partner_ready = shared_state.get(partner_ready_key, False)
        
        if partner_ready:
            st.sidebar.success(f"🟢 {selected_partner.title()} is ready!")
        else:
            st.sidebar.warning(f"🟡 {selected_partner.title()} not ready yet")
            st.sidebar.caption(f"Make sure {selected_partner.title()} is running their interface")
    else:
        st.sidebar.info("Enter a partner name to begin")
    
    # Configuration
    st.sidebar.subheader("Configuration")
    num_qubits = st.sidebar.slider("Number of Qubits", 10, 150, 20)
    prep_method = st.sidebar.selectbox("Preparation Method", ["random", "manual"])
    eve_present = st.sidebar.checkbox("Simulate Eavesdropper", value=shared_state.get("eve_present", False))
    
    # Update eavesdropper setting
    if eve_present != shared_state.get("eve_present", False):
        shared_state["eve_present"] = eve_present
        save_shared_state(shared_state)
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if not selected_partner:
            st.info("👋 **Enter a partner name in the sidebar to start the quantum protocol**")
            st.markdown("""
            **Available Partners:**
            - Bob (port 8502)
            - Huot (port 8503)
            - Or any custom name you agree on
            """)
        else:
            st.markdown(f"### 📨 Communication with {selected_partner.title()}")
            
            # Greeting Phase
            if shared_state["phase"] == "greeting":
                st.info(f"👋 **Step 1:** Send a greeting to {selected_partner.title()}")
                
                alice_message = st.text_input("Message to partner:", 
                                            value=f"Hello {selected_partner.title()}! Ready for quantum key exchange?",
                                            key="alice_msg")
                
                if st.button(f"📤 Send Greeting to {selected_partner.title()}"):
                    shared_state["alice_message"] = alice_message
                    shared_state["alice_ready"] = True
                    shared_state["phase"] = f"waiting_{selected_partner}_response"
                    save_shared_state(shared_state)
                    st.success(f"✅ Greeting sent to {selected_partner.title()}! Waiting for response...")
                    st.rerun()
        
            # Waiting for partner's response
            elif shared_state["phase"] == f"waiting_{selected_partner}_response":
                st.warning(f"⏳ **Waiting for {selected_partner.title()}'s response...**")
                st.info(f"**Your message:** {shared_state['alice_message']}")
                
                partner_ready = shared_state.get(f"{selected_partner}_ready", False)
                if partner_ready:
                    partner_message = shared_state.get(f"{selected_partner}_message", "Ready!")
                    st.success(f"✅ **{selected_partner.title()} responded:** {partner_message}")
                    if st.button("🚀 Start Quantum Protocol"):
                        shared_state["phase"] = "preparation"
                        save_shared_state(shared_state)
                        st.rerun()
        
            # Quantum Protocol Phases
            elif shared_state["phase"] == "preparation":
                st.success(f"🎯 **Step 2:** Prepare qubits for transmission to {selected_partner.title()}")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("🎲 Prepare Qubits"):
                        with st.spinner("Preparing qubits..."):
                            bits, bases = generate_qubits(num_qubits, prep_method)
                            shared_state["alice_bits"] = bits
                            shared_state["alice_bases"] = bases
                            shared_state["phase"] = "transmission"
                            save_shared_state(shared_state)
                        st.success(f"✅ Prepared {num_qubits} qubits!")
                        st.rerun()
                
                with col_b:
                    st.metric("Qubits to prepare", num_qubits)
            
            elif shared_state["phase"] == "transmission":
                st.success(f"📡 **Step 3:** Transmit qubits to {selected_partner.title()}")
                
                if st.button("🚀 Send Qubits"):
                    with st.spinner("Transmitting qubits..."):
                        time.sleep(2)  # Simulate transmission
                        shared_state["phase"] = f"waiting_{selected_partner}_measurement"
                        save_shared_state(shared_state)
                    st.success("✅ Qubits transmitted!")
                    st.rerun()
            
            elif shared_state["phase"] == f"waiting_{selected_partner}_measurement":
                st.warning(f"⏳ **Waiting for {selected_partner.title()} to measure qubits...**")
                partner_results = shared_state.get(f"{selected_partner}_results")
                if partner_results:
                    st.success(f"✅ {selected_partner.title()} completed measurements!")
                    if st.button("🔍 Start Sifting Process"):
                        shared_state["phase"] = "sifting"
                        save_shared_state(shared_state)
                        st.rerun()
            
            elif shared_state["phase"] == "sifting":
                st.success(f"🔍 **Step 4:** Compare bases and sift keys with {selected_partner.title()}")
                
                if st.button("🔀 Perform Sifting"):
                    with st.spinner("Comparing bases..."):
                        partner_bases = shared_state.get(f"{selected_partner}_bases", [])
                        partner_results = shared_state.get(f"{selected_partner}_results", [])
                        
                        sifted_bits, matching_indices = perform_sifting(
                            shared_state["alice_bits"],
                            shared_state["alice_bases"],
                            partner_bases,
                            partner_results
                        )
                        shared_state["sifted_bits"] = sifted_bits
                        shared_state["matching_indices"] = matching_indices
                        shared_state["phase"] = "error_check"
                        save_shared_state(shared_state)
                    st.success(f"✅ Sifting complete with {selected_partner.title()}! {len(sifted_bits)} matching bits")
                    st.rerun()
            
            elif shared_state["phase"] == "error_check":
                st.success(f"⚠️ **Step 5:** Check for transmission errors with {selected_partner.title()}")
                
                if st.button("🔍 Check Errors"):
                    with st.spinner("Checking for errors..."):
                        error_rate, errors, remaining_bits = error_checking(
                            shared_state["alice_bits"],
                            shared_state["sifted_bits"],
                            shared_state["matching_indices"],
                            shared_state["eve_present"]
                        )
                        shared_state["error_rate"] = error_rate
                        shared_state["sifted_bits"] = remaining_bits
                        shared_state["phase"] = "key_generation"
                        save_shared_state(shared_state)
                    st.success(f"✅ Error check complete! Rate: {error_rate:.3f}")
                    st.rerun()
            
            elif shared_state["phase"] == "key_generation":
                st.success(f"🔑 **Step 6:** Generate final quantum key with {selected_partner.title()}")
                
                # Show debug info before key generation
                sifted_count = len(shared_state.get("sifted_bits", []))
                st.info(f"📊 Available bits for key generation: {sifted_count}")
                
                if sifted_count < 4:
                    st.error(f"❌ Not enough bits! Have {sifted_count}, need at least 4")
                    st.info("💡 Try restarting with more qubits (40-50) or disable eavesdropper")
                    
                    # Add recovery options
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("🔄 Restart Protocol"):
                            if SHARED_STATE_FILE.exists():
                                SHARED_STATE_FILE.unlink()
                            st.rerun()
                    
                    with col_b:
                        if st.button("⏪ Back to Error Check"):
                            shared_state["phase"] = "error_check"
                            save_shared_state(shared_state)
                            st.rerun()
                else:
                    if st.button("🔐 Generate Key"):
                        with st.spinner("Generating final key..."):
                            final_key = generate_final_key(shared_state["sifted_bits"])
                            if final_key:
                                shared_state["final_key"] = final_key
                                shared_state["phase"] = "complete"
                                save_shared_state(shared_state)
                                st.success("✅ Quantum key generated!")
                                st.balloons()
                            else:
                                st.error("❌ Key generation failed!")
                                st.error(f"Debug: Bits = {shared_state['sifted_bits'][:10]}...")
                        st.rerun()
            
            elif shared_state["phase"] == "complete":
                st.success("🎉 **Protocol Complete!**")
                st.balloons()
    
    with col2:
        st.markdown("### 📊 Alice's Data")
        
        # Current status
        phase_status = {
            "greeting": f"📝 Ready to send greeting to {selected_partner.title()}",
            f"waiting_{selected_partner}_response": f"⏳ Waiting for {selected_partner.title()}",
            "preparation": "🎲 Ready to prepare qubits",
            "transmission": "📡 Ready to transmit",
            f"waiting_{selected_partner}_measurement": f"⏳ Waiting for {selected_partner.title()}",
            "sifting": "🔍 Ready to sift",
            "error_check": "⚠️ Ready for error check",
            "key_generation": "🔑 Ready for key gen",
            "complete": "✅ Complete"
        }
        
        st.info(f"**Status:** {phase_status.get(shared_state['phase'], 'Unknown')}")
        if selected_partner:
            st.info(f"**Partner:** {selected_partner.title()}")
        else:
            st.info("**Partner:** None selected")
        
        # Alice's qubits data
        if shared_state.get("alice_bits"):
            st.subheader("🎭 Prepared Qubits")
            
            # Show sample data with proper length handling
            alice_bits = shared_state["alice_bits"]
            alice_bases = shared_state.get("alice_bases", [])
            
            # Ensure arrays have same length and valid data
            if alice_bits and alice_bases:
                min_length = min(len(alice_bits), len(alice_bases))
                sample_size = min(10, min_length)
                
                if sample_size > 0:
                    # Validate data before creating DataFrame
                    valid_bits = alice_bits[:sample_size]
                    valid_bases = alice_bases[:sample_size]
                    
                    # Ensure both arrays have exactly the same length
                    if len(valid_bits) == len(valid_bases) == sample_size:
                        df_alice = pd.DataFrame({
                            'Q#': range(1, sample_size + 1),
                            'Bit': valid_bits,
                            'Basis': ['+' if b == 0 else '×' for b in valid_bases]
                        })
                        st.dataframe(df_alice, use_container_width=True)
                        
                        if len(alice_bits) > sample_size:
                            st.caption(f"Showing {sample_size} of {len(alice_bits)} qubits")
                    else:
                        st.warning("⚠️ Data validation issue - lengths don't match")
                else:
                    st.info("No valid qubit data available yet.")
            else:
                st.info("Waiting for qubit data...")
        
        # Statistics
        if shared_state.get("sifted_bits"):
            st.subheader("📈 Protocol Stats")
            
            total_qubits = len(shared_state.get("alice_bits", []))
            sifted_count = len(shared_state["sifted_bits"])
            
            st.metric("Total Qubits", total_qubits)
            st.metric("Sifted Bits", sifted_count)
            
            if shared_state.get("error_rate"):
                st.metric("Error Rate", f"{shared_state['error_rate']:.3f}")
    
    # Visualization
    if shared_state.get("alice_bits") and shared_state.get("alice_bases"):
        st.markdown("### 📈 Alice's Quantum Data Visualization")
        
        alice_bits = shared_state["alice_bits"]
        alice_bases = shared_state["alice_bases"]
        
        # Ensure arrays have same length for visualization
        min_length = min(len(alice_bits), len(alice_bases))
        display_limit = min(50, min_length)
        
        if display_limit > 0:
            fig = go.Figure()
            
            x_vals = list(range(1, display_limit + 1))
            
            # Alice's bits
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=alice_bits[:display_limit],
                mode='markers+lines',
                name='Bit Values',
                marker=dict(color='pink', size=8),
                line=dict(color='hotpink', width=2)
            ))
            
            # Alice's bases
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=alice_bases[:display_limit],
                mode='markers+lines',
                name='Basis Choice',
                marker=dict(color='lightcoral', size=8),
                line=dict(color='red', width=2),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title="Alice's Prepared Qubits",
                xaxis_title="Qubit Number",
                yaxis=dict(title="Bit Value", side="left"),
                yaxis2=dict(title="Basis (0=+, 1=×)", overlaying="y", side="right"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Final key display
    if shared_state.get("final_key"):
        st.markdown("### 🔑 Generated Quantum Key")
        
        st.success("✅ **Shared Secret Key Generated!**")
        
        # Key display with copy functionality
        key_container = st.container()
        with key_container:
            st.code(shared_state["final_key"], language="text")
        
        # Chat Demo Link
        st.markdown("---")
        st.markdown("### 🚀 **Alice: Ready for Quantum Chat!**")
        
        # Create clickable link with Alice's styling
        st.markdown("""
        <div style='text-align: center; margin: 20px 0;'>
            <a href="http://localhost:3000" target="_blank" style='
                display: inline-block;
                background: linear-gradient(45deg, #ff69b4, #ff1493);
                color: #fff;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 18px;
                text-transform: uppercase;
                letter-spacing: 2px;
                box-shadow: 0 0 20px rgba(255, 105, 180, 0.5);
                transition: all 0.3s ease;
            '>
                🎭 ALICE: JOIN QUANTUM CHAT
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Security assessment
        error_rate = shared_state.get("error_rate", 0)
        if error_rate > 0.15:
            st.error("🚨 **HIGH ERROR RATE!** Channel may be compromised.")
            if shared_state.get("eve_present"):
                st.success("✅ Eavesdropper correctly detected!")
        elif error_rate > 0.05:
            st.warning("⚠️ **Moderate error rate.** Investigate further.")
        else:
            st.success("🔒 **Low error rate.** Channel secure.")
        
        # Instructions
        st.info(f"""
        **🎯 Alice's Next Steps:**
        1. Click "Alice: Join Quantum Chat" above
        2. Enter username as "Alice" 
        3. Paste your quantum key
        4. Wait for {selected_partner.title()} to join with the same key
        5. Send encrypted messages securely!
        """)
        
        # Reset option
        if st.button("🔄 Start New Protocol"):
            if SHARED_STATE_FILE.exists():
                SHARED_STATE_FILE.unlink()
            st.rerun()
    
    # Auto-refresh for real-time updates
    waiting_phases = [f"waiting_{selected_partner}_response", f"waiting_{selected_partner}_measurement"]
    if shared_state["phase"] in waiting_phases:
        time.sleep(2)
        st.rerun()
    
    # Footer
    st.markdown("---")
    partner_info = f"Current Partner: <strong>{selected_partner.title()}</strong>" if selected_partner else "No partner selected"
    st.markdown(f"""
    <div style='text-align: center; color: #ff69b4;'>
    <p><strong>🎭 Alice's Quantum Terminal</strong></p>
    <p>{partner_info}</p>
    <p>Available: Bob (8502) | Huot (8503) | Custom names</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
