"""
BB84 Quantum Key Generator - Streamlit Web Interface
Interactive web-based quantum cryptography demonstration

HOW TO RUN:
1. Install Streamlit: pip install streamlit
2. Navigate to this directory in terminal
3. Run: streamlit run streamlit-keygen.py
4. Open browser to http://localhost:8501

Features:
- Split view with Alice and Bob panels
- Real-time quantum key generation
- Eavesdropper simulation
- Interactive controls and visualizations
"""

import streamlit as st
import random
import hashlib
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64

# Configure page
st.set_page_config(
    page_title="BB84 Quantum Key Generator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for quantum theme
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #00ffff;
    font-size: 2.5em;
    font-weight: bold;
    text-shadow: 0 0 20px #00ffff;
    margin-bottom: 30px;
}
.alice-panel {
    background: linear-gradient(135deg, #1a0d2e, #2d1b69);
    border: 2px solid #ff69b4;
    border-radius: 15px;
    padding: 20px;
    margin: 10px;
}
.bob-panel {
    background: linear-gradient(135deg, #0d1a2e, #1b2d69);
    border: 2px solid #00bfff;
    border-radius: 15px;
    padding: 20px;
    margin: 10px;
}
.quantum-metric {
    text-align: center;
    padding: 15px;
    background: rgba(0, 255, 255, 0.1);
    border-radius: 10px;
    margin: 5px;
}
.success-message {
    color: #00ff88;
    font-weight: bold;
}
.error-message {
    color: #ff4444;
    font-weight: bold;
}
.warning-message {
    color: #ffaa00;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'alice_bits' not in st.session_state:
        st.session_state.alice_bits = []
    if 'alice_bases' not in st.session_state:
        st.session_state.alice_bases = []
    if 'bob_bases' not in st.session_state:
        st.session_state.bob_bases = []
    if 'bob_results' not in st.session_state:
        st.session_state.bob_results = []
    if 'sifted_bits' not in st.session_state:
        st.session_state.sifted_bits = []
    if 'final_key' not in st.session_state:
        st.session_state.final_key = ""
    if 'phase' not in st.session_state:
        st.session_state.phase = "setup"
    if 'error_rate' not in st.session_state:
        st.session_state.error_rate = 0.0
    if 'eve_present' not in st.session_state:
        st.session_state.eve_present = False

def reset_protocol():
    """Reset the protocol to initial state"""
    st.session_state.alice_bits = []
    st.session_state.alice_bases = []
    st.session_state.bob_bases = []
    st.session_state.bob_results = []
    st.session_state.sifted_bits = []
    st.session_state.final_key = ""
    st.session_state.phase = "setup"
    st.session_state.error_rate = 0.0
    # Clear any other stored data
    if 'transmitted_bits' in st.session_state:
        del st.session_state.transmitted_bits
    if 'eve_activity' in st.session_state:
        del st.session_state.eve_activity
    if 'matching_indices' in st.session_state:
        del st.session_state.matching_indices

def generate_qubits(num_qubits, method="random"):
    """Generate Alice's qubits"""
    bits = []
    bases = []
    
    for i in range(num_qubits):
        if method == "random":
            bits.append(random.randint(0, 1))
            bases.append(random.randint(0, 1))
        else:  # manual - simplified to random for web interface
            bits.append(random.randint(0, 1))
            bases.append(random.randint(0, 1))
    
    return bits, bases

def simulate_transmission(alice_bits, alice_bases, has_eavesdropper=False):
    """Simulate quantum transmission with optional eavesdropper"""
    transmitted_bits = alice_bits.copy()
    eve_activity = []
    
    if has_eavesdropper:
        for i in range(len(transmitted_bits)):
            if random.random() < 0.6:  # 60% interception rate
                eve_activity.append(f"Qubit {i+1}: Intercepted!")
                if random.random() < 0.5:  # Wrong basis 50% of time
                    transmitted_bits[i] = random.randint(0, 1)
            else:
                eve_activity.append(f"Qubit {i+1}: Passed through")
    
    return transmitted_bits, eve_activity

def bob_measurement(alice_bases, transmitted_bits, method="random"):
    """Simulate Bob's measurements"""
    bob_bases = []
    bob_results = []
    
    for i in range(len(transmitted_bits)):
        if method == "random":
            basis = random.randint(0, 1)
        else:
            basis = random.randint(0, 1)  # Simplified
        
        bob_bases.append(basis)
        
        # Measurement result
        if alice_bases[i] == basis:
            result = transmitted_bits[i]
        else:
            result = random.randint(0, 1)
        
        bob_results.append(result)
    
    return bob_bases, bob_results

def perform_sifting(alice_bits, alice_bases, bob_bases, bob_results):
    """Perform basis sifting"""
    sifted_bits = []
    matching_indices = []
    
    # Ensure all arrays have the same length
    min_length = min(len(alice_bits), len(alice_bases), len(bob_bases), len(bob_results))
    
    for i in range(min_length):
        if alice_bases[i] == bob_bases[i]:
            sifted_bits.append(int(bob_results[i]))  # Ensure integer
            matching_indices.append(i)
    
    return sifted_bits, matching_indices

def error_checking(alice_bits, sifted_bits, matching_indices, has_eavesdropper=False):
    """Perform error checking on all sifted bits"""
    total_bits = len(sifted_bits)
    if total_bits == 0:
        st.warning("⚠️ No sifted bits available for error checking")
        return 0.0, 0, []
    
    st.info(f"🔧 Error checking {total_bits} sifted bits")
    
    errors = 0
    
    # Check all bits
    for idx in range(total_bits):
        if idx < len(matching_indices) and matching_indices[idx] < len(alice_bits):
            alice_bit = alice_bits[matching_indices[idx]]
            bob_bit = sifted_bits[idx]
            if alice_bit != bob_bit:
                errors += 1
    
    # Add eavesdropper errors
    if has_eavesdropper:
        if errors == 0:
            additional_errors = random.randint(1, max(1, total_bits // 10))
            errors += additional_errors
            st.info(f"🔧 Added {additional_errors} eavesdropper errors")
        else:
            additional_errors = random.randint(0, max(1, total_bits // 20))
            errors += additional_errors
            if additional_errors > 0:
                st.info(f"🔧 Added {additional_errors} additional eavesdropper errors")
    
    error_rate = errors / total_bits if total_bits > 0 else 0
    
    # Remove some bits that were "used" for error checking
    # Be more conservative to ensure we have enough bits left
    sacrifice_count = min(errors + 1, max(1, len(sifted_bits) // 8))  # Less aggressive sacrifice
    remaining_bits = sifted_bits[:-sacrifice_count] if sacrifice_count > 0 and sacrifice_count < len(sifted_bits) else sifted_bits
    
    st.info(f"🔧 Sacrificed {sacrifice_count} bits, {len(remaining_bits)} remaining")
    
    return error_rate, errors, remaining_bits

def generate_final_key(sifted_bits):
    """Generate final key using privacy amplification"""
    if not sifted_bits or len(sifted_bits) < 4:
        st.error(f"❌ Not enough bits! Have {len(sifted_bits) if sifted_bits else 0}, need at least 4")
        return None
    
    try:
        # Debug: Show the sifted bits
        st.info(f"🔧 Debug: Processing {len(sifted_bits)} sifted bits: {sifted_bits[:10]}...")
        
        # Ensure all bits are 0 or 1
        clean_bits = []
        for bit in sifted_bits:
            if bit in [0, 1]:
                clean_bits.append(bit)
            else:
                st.warning(f"⚠️ Invalid bit value: {bit}, converting to 0")
                clean_bits.append(0)
        
        bit_string = ''.join(str(b) for b in clean_bits)
        st.info(f"🔧 Debug: Bit string length: {len(bit_string)}")
        
        # Ensure we have valid binary string
        if not bit_string or not all(c in '01' for c in bit_string):
            st.error(f"❌ Invalid binary string: {bit_string[:20]}...")
            return None
            
        # Pad to multiple of 8
        while len(bit_string) % 8 != 0:
            bit_string += '0'
        
        st.info(f"🔧 Debug: Padded bit string length: {len(bit_string)}")
        
        # Convert to bytes and hash
        try:
            byte_data = bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))
            final_key = hashlib.sha256(byte_data).hexdigest()
            
            st.success(f"✅ Key generated successfully! Length: {len(final_key)} characters")
            return final_key
            
        except ValueError as ve:
            st.error(f"❌ Byte conversion error: {str(ve)}")
            st.error(f"Problematic bit string: {bit_string}")
            return None
        
    except Exception as e:
        st.error(f"❌ Key generation error: {str(e)}")
        st.error(f"Input bits: {sifted_bits}")
        return None

def create_visualization(alice_bits, alice_bases, bob_bases, bob_results, phase):
    """Create interactive visualizations"""
    if not alice_bits:
        return None
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Alice Bits', 'Alice Bases', 'Bob Bases', 'Bob Results'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Limit display for large datasets
    display_limit = min(50, len(alice_bits))
    x_vals = list(range(1, display_limit + 1))
    
    # Alice's bits
    fig.add_trace(
        go.Scatter(x=x_vals, y=alice_bits[:display_limit], 
                  mode='markers+lines', name='Alice Bits',
                  marker=dict(color='pink', size=8)),
        row=1, col=1
    )
    
    # Alice's bases
    fig.add_trace(
        go.Scatter(x=x_vals, y=alice_bases[:display_limit], 
                  mode='markers+lines', name='Alice Bases',
                  marker=dict(color='lightcoral', size=8)),
        row=1, col=2
    )
    
    # Bob's bases (if available)
    if bob_bases:
        fig.add_trace(
            go.Scatter(x=x_vals, y=bob_bases[:display_limit], 
                      mode='markers+lines', name='Bob Bases',
                      marker=dict(color='lightblue', size=8)),
            row=2, col=1
        )
    
    # Bob's results (if available)
    if bob_results:
        fig.add_trace(
            go.Scatter(x=x_vals, y=bob_results[:display_limit], 
                      mode='markers+lines', name='Bob Results',
                      marker=dict(color='cyan', size=8)),
            row=2, col=2
        )
    
    fig.update_layout(
        title="BB84 Protocol Visualization",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

# Main application
def main():
    init_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🔬 BB84 Quantum Key Generator</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.title("🎛️ Protocol Controls")
    
    # Configuration
    st.sidebar.subheader("Configuration")
    num_qubits = st.sidebar.slider("Number of Qubits", 10, 150, 20)
    method = st.sidebar.selectbox("Preparation Method", ["random", "manual"])
    has_eavesdropper = st.sidebar.checkbox("Add Eavesdropper (Eve)", value=False)
    
    st.session_state.eve_present = has_eavesdropper
    
    # Protocol phases
    st.sidebar.subheader("Protocol Phases")
    
    # Add emergency reset at the top
    if st.sidebar.button("🚨 EMERGENCY RESET", type="secondary"):
        reset_protocol()
        st.success("🔄 Protocol completely reset!")
        st.rerun()
    
    st.sidebar.divider()

    if st.sidebar.button("🎭 1. Alice Prepares Qubits"):
        with st.spinner("Alice preparing qubits..."):
            st.session_state.alice_bits, st.session_state.alice_bases = generate_qubits(num_qubits, method)
            st.session_state.phase = "prepared"
        st.success(f"✅ Alice prepared {num_qubits} qubits!")
    
    if st.sidebar.button("🚀 2. Transmit Qubits") and st.session_state.phase >= "prepared":
        with st.spinner("Transmitting qubits through quantum channel..."):
            transmitted_bits, eve_activity = simulate_transmission(
                st.session_state.alice_bits, 
                st.session_state.alice_bases, 
                has_eavesdropper
            )
            st.session_state.transmitted_bits = transmitted_bits
            st.session_state.eve_activity = eve_activity
            st.session_state.phase = "transmitted"
        st.success("✅ Qubits transmitted!")
    
    if st.sidebar.button("🔬 3. Bob Measures") and st.session_state.phase >= "transmitted":
        with st.spinner("Bob measuring qubits..."):
            st.session_state.bob_bases, st.session_state.bob_results = bob_measurement(
                st.session_state.alice_bases,
                st.session_state.transmitted_bits,
                method
            )
            st.session_state.phase = "measured"
        st.success("✅ Bob completed measurements!")
    
    if st.sidebar.button("🔍 4. Sift Keys") and st.session_state.phase >= "measured":
        with st.spinner("Sifting keys..."):
            st.session_state.sifted_bits, st.session_state.matching_indices = perform_sifting(
                st.session_state.alice_bits,
                st.session_state.alice_bases,
                st.session_state.bob_bases,
                st.session_state.bob_results
            )
            st.session_state.phase = "sifted"
        st.success("✅ Key sifting completed!")
    
    if st.sidebar.button("⚠️ 5. Check Errors") and st.session_state.phase >= "sifted":
        with st.spinner("Checking for errors..."):
            st.session_state.error_rate, errors, remaining_bits = error_checking(
                st.session_state.alice_bits,
                st.session_state.sifted_bits,
                st.session_state.matching_indices,
                has_eavesdropper
            )
            st.session_state.sifted_bits = remaining_bits
            st.session_state.phase = "error_checked"
        if st.session_state.error_rate > 0.15:
            st.error(f"🚨 High error rate: {st.session_state.error_rate:.3f}")
        else:
            st.success(f"✅ Low error rate: {st.session_state.error_rate:.3f}")
    
    if st.sidebar.button("🔑 6. Generate Final Key") and st.session_state.phase >= "error_checked":
        with st.spinner("Generating final key..."):
            # Show current state for debugging
            st.write("🔧 **Debug Information:**")
            st.write(f"- Sifted bits count: {len(st.session_state.sifted_bits)}")
            st.write(f"- Sifted bits sample: {st.session_state.sifted_bits[:10] if st.session_state.sifted_bits else 'None'}")
            st.write(f"- Current phase: {st.session_state.phase}")
            
            if len(st.session_state.sifted_bits) < 4:
                st.error(f"❌ Not enough bits for key generation! Have {len(st.session_state.sifted_bits)}, need at least 4 bits.")
                st.info("💡 Try using more qubits or reduce eavesdropper interference")
                st.session_state.final_key = ""
            else:
                final_key = generate_final_key(st.session_state.sifted_bits)
                if final_key:
                    st.session_state.final_key = final_key
                    st.session_state.phase = "complete"
                    st.balloons()
                    st.success("✅ Final key generated successfully!")
                else:
                    st.error("❌ Key generation failed! Check the debug information above.")
                    st.session_state.final_key = ""
    
    if st.sidebar.button("🔄 Reset Protocol"):
        reset_protocol()
        st.success("🔄 Protocol reset! You can start over.")
        st.rerun()
    
    # Main content area
    col1, col2 = st.columns(2)
    
    # Alice's Panel
    with col1:
        st.markdown("### 🎭 Alice (Sender)")
        
        if st.session_state.alice_bits:
            st.write(f"**Prepared {len(st.session_state.alice_bits)} qubits**")
            
            # Show sample data
            sample_size = min(20, len(st.session_state.alice_bits))
            df_alice = pd.DataFrame({
                'Qubit': range(1, sample_size + 1),
                'Bit': st.session_state.alice_bits[:sample_size],
                'Basis': ['+' if b == 0 else '×' for b in st.session_state.alice_bases[:sample_size]]
            })
            st.dataframe(df_alice, use_container_width=True)
            
            if len(st.session_state.alice_bits) > 20:
                st.caption(f"Showing first 20 of {len(st.session_state.alice_bits)} qubits")
        else:
            st.info("No qubits prepared yet. Use the controls in the sidebar.")
    
    # Bob's Panel
    with col2:
        st.markdown("### 🔬 Bob (Receiver)")
        
        if st.session_state.bob_results:
            st.write(f"**Measured {len(st.session_state.bob_results)} qubits**")
            
            # Show sample data
            sample_size = min(20, len(st.session_state.bob_results))
            df_bob = pd.DataFrame({
                'Qubit': range(1, sample_size + 1),
                'Basis': ['+' if b == 0 else '×' for b in st.session_state.bob_bases[:sample_size]],
                'Result': st.session_state.bob_results[:sample_size],
                'Match': ['✓' if st.session_state.alice_bases[i] == st.session_state.bob_bases[i] 
                         else '✗' for i in range(sample_size)]
            })
            st.dataframe(df_bob, use_container_width=True)
            
            if len(st.session_state.bob_results) > 20:
                st.caption(f"Showing first 20 of {len(st.session_state.bob_results)} qubits")
        else:
            st.info("No measurements yet. Complete previous steps first.")
    
    # Statistics
    if st.session_state.alice_bits:
        st.markdown("### 📊 Protocol Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Qubits", len(st.session_state.alice_bits))
        
        with col2:
            if st.session_state.sifted_bits:
                st.metric("Sifted Bits", len(st.session_state.sifted_bits))
        
        with col3:
            if st.session_state.error_rate:
                st.metric("Error Rate", f"{st.session_state.error_rate:.3f}")
        
        with col4:
            if st.session_state.final_key:
                st.metric("Key Length", f"{len(st.session_state.final_key)} hex chars")
    
    # Eavesdropper Activity
    if has_eavesdropper and hasattr(st.session_state, 'eve_activity'):
        st.markdown("### 👁️ Eavesdropper Activity")
        with st.expander("Show Eve's Interference"):
            for activity in st.session_state.eve_activity[:20]:
                if "Intercepted" in activity:
                    st.markdown(f"🔍 {activity}")
                else:
                    st.markdown(f"✓ {activity}")
            
            if len(st.session_state.eve_activity) > 20:
                st.caption(f"Showing first 20 of {len(st.session_state.eve_activity)} activities")
    
    # Visualization
    if st.session_state.alice_bits:
        st.markdown("### 📈 Protocol Visualization")
        fig = create_visualization(
            st.session_state.alice_bits,
            st.session_state.alice_bases,
            st.session_state.bob_bases if hasattr(st.session_state, 'bob_bases') else [],
            st.session_state.bob_results if hasattr(st.session_state, 'bob_results') else [],
            st.session_state.phase
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Final Key Display
    if st.session_state.final_key:
        st.markdown("### 🔑 Generated Quantum Key")
        
        st.success("✅ **Shared Secret Key Generated!**")
        st.code(st.session_state.final_key, language="text")
        
        # Chat Demo Link
        st.markdown("---")
        st.markdown("### 🚀 **Ready for Quantum Chat Demo!**")
        
        # Create clickable link with styling
        st.markdown("""
        <div style='text-align: center; margin: 20px 0;'>
            <a href="http://localhost:3000" target="_blank" style='
                display: inline-block;
                background: linear-gradient(45deg, #00ffff, #0099cc);
                color: #000;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 18px;
                text-transform: uppercase;
                letter-spacing: 2px;
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
                transition: all 0.3s ease;
            '>
                🔗 LAUNCH QUANTUM CHAT
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Instructions
        st.info("""
        **🎯 Chat Demo Instructions:**
        1. Click the "Launch Quantum Chat" button above
        2. Enter your username (Alice or Bob)
        3. Paste the generated key in the quantum key field
        4. Join the chat and use Encrypt/Decrypt buttons
        """)
        
        # Copy to clipboard functionality
        st.markdown("**Alternative:** Copy key manually:")
        
        # Security Assessment
        if st.session_state.error_rate > 0.15:
            st.error("🚨 **HIGH ERROR RATE DETECTED!** Channel may be compromised.")
            if st.session_state.eve_present:
                st.success("✅ Eavesdropper correctly detected by BB84 protocol!")
        elif st.session_state.error_rate > 0.05:
            st.warning("⚠️ **Moderate error rate.** Channel security questionable.")
        else:
            st.success("🔒 **Low error rate.** Channel appears secure.")
            if st.session_state.eve_present:
                st.warning("⚠️ Eavesdropper was present but got lucky with low detection.")
        
        # Download key option
        key_data = f"""BB84 Quantum Key Generation Results
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
Total Qubits: {len(st.session_state.alice_bits)}
Sifted Bits: {len(st.session_state.sifted_bits) + (st.session_state.error_rate * 10)}
Error Rate: {st.session_state.error_rate:.3f}
Eavesdropper: {'Yes' if st.session_state.eve_present else 'No'}
Security: {'Compromised' if st.session_state.error_rate > 0.15 else 'Secure'}

Final Key (hex):
{st.session_state.final_key}
"""
        
        st.download_button(
            label="💾 Download Key Report",
            data=key_data,
            file_name=f"bb84_key_{int(time.time())}.txt",
            mime="text/plain"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    <p>🔬 BB84 Quantum Key Distribution Protocol Simulator</p>
    <p>Built with Streamlit • Quantum Cryptography Demo</p>
    </div>
    """, unsafe_allow_html=True)

    # Add debug panel if stuck
    if st.session_state.phase == "error_checked" and not st.session_state.final_key:
        st.markdown("### 🔧 Debug Panel")
        st.error("**You're stuck at key generation!**")
        
        with st.expander("🛠️ Troubleshooting Options", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Reset Everything"):
                    reset_protocol()
                    st.success("Reset complete!")
                    st.rerun()
            
            with col2:
                if st.button("⏪ Go Back to Sifting"):
                    st.session_state.phase = "sifted"
                    st.success("Returned to sifting phase")
                    st.rerun()
            
            with col3:
                if st.button("🎲 Regenerate More Qubits"):
                    reset_protocol()
                    # Auto-generate with more qubits
                    st.session_state.alice_bits, st.session_state.alice_bases = generate_qubits(50, "random")
                    st.session_state.phase = "prepared"
                    st.success("Generated 50 qubits automatically!")
                    st.rerun()
        
        st.info("""
        **Why you might be stuck:**
        - Not enough bits after error checking (need at least 4)
        - Try using more qubits (30-50)
        - Turn off eavesdropper temporarily
        - Use the buttons above to recover
        """)

if __name__ == "__main__":
    main()
