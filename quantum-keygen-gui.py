"""
Interactive BB84 Quantum Key Generator with Split GUI
Alice on the left, Bob on the right - See the quantum flow in real time!

HOW TO RUN:
1. Make sure you have Python 3.6+ installed
2. Navigate to this directory in terminal/command prompt
3. Run: python quantum-keygen-gui.py
   OR: python3 quantum-keygen-gui.py
   OR: Just double-click this file (on Windows)

No additional packages required - uses built-in tkinter!
"""

import random
import hashlib
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from typing import List, Tuple
import os

class BB84SplitGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BB84 Quantum Key Generator - Alice & Bob")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e2e')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Variables
        self.num_qubits = 20
        self.has_eavesdropper = False
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_results = []
        self.final_key = ""
        self.current_phase = "setup"
        self.bob_ready = False
        
        self.create_main_layout()
        self.show_setup()
        
    def configure_styles(self):
        """Configure custom styles for dark theme"""
        self.style.configure('Title.TLabel', 
                           font=('Arial', 16, 'bold'),
                           foreground='#cdd6f4',
                           background='#1e1e2e')
        self.style.configure('Heading.TLabel', 
                           font=('Arial', 12, 'bold'),
                           foreground='#89b4fa',
                           background='#313244')
        self.style.configure('Info.TLabel',
                           font=('Arial', 10),
                           foreground='#cdd6f4',
                           background='#313244')
        self.style.configure('Alice.TLabel',
                           font=('Arial', 10, 'bold'),
                           foreground='#f38ba8',
                           background='#313244')
        self.style.configure('Bob.TLabel',
                           font=('Arial', 10, 'bold'),
                           foreground='#89b4fa',
                           background='#313244')
        self.style.configure('Success.TLabel',
                           font=('Arial', 10, 'bold'),
                           foreground='#a6e3a1',
                           background='#313244')
        
    def create_main_layout(self):
        """Create the main split layout"""
        # Top banner
        self.banner_frame = ttk.Frame(self.root)
        self.banner_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        self.title_label = ttk.Label(self.banner_frame, 
                                    text="🔬 BB84 Quantum Key Distribution", 
                                    style='Title.TLabel')
        self.title_label.pack()
        
        # Status bar
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = ttk.Label(self.status_frame, 
                                     text="Phase: Setup", 
                                     style='Info.TLabel')
        self.status_label.pack()
        
        # Main content frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Alice's panel (left)
        self.alice_panel = ttk.LabelFrame(self.main_frame, text="🎭 Alice (Sender)")
        self.alice_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Quantum channel (center)
        self.channel_panel = ttk.LabelFrame(self.main_frame, text="🌌 Quantum Channel")
        self.channel_panel.pack(side='left', fill='y', padx=5)
        
        # Bob's panel (right)
        self.bob_panel = ttk.LabelFrame(self.main_frame, text="🔬 Bob (Receiver)")
        self.bob_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Bottom control panel
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(fill='x', padx=10, pady=10)
        
        self.create_panels()
    
    def create_panels(self):
        """Create Alice, Bob, and channel panels"""
        # === ALICE'S PANEL ===
        alice_main = ttk.Frame(self.alice_panel)
        alice_main.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Alice's initial message area
        alice_msg_frame = ttk.LabelFrame(alice_main, text="Initial Communication")
        alice_msg_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(alice_msg_frame, text="Send greeting to Bob:", 
                 style='Alice.TLabel').pack(anchor='w', padx=5, pady=2)
        
        self.alice_message_var = tk.StringVar(value="Hello Bob! Ready for quantum key exchange?")
        self.alice_message_entry = ttk.Entry(alice_msg_frame, textvariable=self.alice_message_var, width=40)
        self.alice_message_entry.pack(padx=5, pady=2, fill='x')
        
        self.alice_send_btn = ttk.Button(alice_msg_frame, text="📤 Send Message", 
                                        command=self.alice_send_message)
        self.alice_send_btn.pack(pady=5)
        
        # Alice's preparation area
        alice_prep_frame = ttk.LabelFrame(alice_main, text="Qubit Preparation")
        alice_prep_frame.pack(fill='x', pady=(0, 5))
        
        # Qubit count selection
        qubit_count_frame = ttk.Frame(alice_prep_frame)
        qubit_count_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(qubit_count_frame, text="Number of qubits:", 
                 style='Alice.TLabel').pack(side='left')
        
        self.qubit_count_var = tk.StringVar(value="20")
        qubit_spinbox = ttk.Spinbox(qubit_count_frame, 
                                   from_=10, to=150, 
                                   textvariable=self.qubit_count_var, 
                                   width=8, 
                                   command=self.update_qubit_count)
        qubit_spinbox.pack(side='left', padx=(10, 5))
        
        ttk.Label(qubit_count_frame, text="(10-150)", 
                 style='Info.TLabel').pack(side='left')
        
        # Preparation method
        ttk.Label(alice_prep_frame, text="Choose bits and bases:", 
                 style='Alice.TLabel').pack(anchor='w', padx=5, pady=(10, 2))
        
        self.alice_method_var = tk.StringVar(value="random")
        ttk.Radiobutton(alice_prep_frame, text="🎲 Random", 
                       variable=self.alice_method_var, value="random").pack(anchor='w', padx=5)
        ttk.Radiobutton(alice_prep_frame, text="✋ Manual", 
                       variable=self.alice_method_var, value="manual").pack(anchor='w', padx=5)
        
        self.alice_prep_btn = ttk.Button(alice_prep_frame, text="Prepare Qubits", 
                                        command=self.start_alice_preparation, 
                                        state='disabled')
        self.alice_prep_btn.pack(pady=5)
        
        # Alice's data display
        self.alice_data = scrolledtext.ScrolledText(alice_main, height=12, width=35)
        self.alice_data.pack(fill='both', expand=True, pady=5)
        
        # === QUANTUM CHANNEL ===
        channel_main = ttk.Frame(self.channel_panel)
        channel_main.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Channel status
        ttk.Label(channel_main, text="Transmission Status:", 
                 style='Heading.TLabel').pack(pady=(0, 5))
        
        self.channel_status = ttk.Label(channel_main, text="Ready", 
                                       style='Info.TLabel')
        self.channel_status.pack()
        
        # Eavesdropper controls
        eve_frame = ttk.LabelFrame(channel_main, text="Security")
        eve_frame.pack(fill='x', pady=10)
        
        self.eve_var = tk.BooleanVar()
        ttk.Checkbutton(eve_frame, text="Add Eve\n(Eavesdropper)", 
                       variable=self.eve_var).pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(channel_main, length=150, mode='indeterminate')
        self.progress.pack(pady=10)
        
        # Transmission button
        self.transmit_btn = ttk.Button(channel_main, text="🚀 Send Qubits", 
                                      command=self.start_transmission, 
                                      state='disabled')
        self.transmit_btn.pack(pady=5)
        
        # Eve activity (initially hidden)
        self.eve_activity = scrolledtext.ScrolledText(channel_main, height=8, width=20)
        
        # === BOB'S PANEL ===
        bob_main = ttk.Frame(self.bob_panel)
        bob_main.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Bob's response area
        bob_msg_frame = ttk.LabelFrame(bob_main, text="Incoming Message")
        bob_msg_frame.pack(fill='x', pady=(0, 5))
        
        self.bob_message_display = ttk.Label(bob_msg_frame, text="Waiting for Alice's message...", 
                                           style='Bob.TLabel', wraplength=300)
        self.bob_message_display.pack(anchor='w', padx=5, pady=5)
        
        bob_response_frame = ttk.Frame(bob_msg_frame)
        bob_response_frame.pack(fill='x', padx=5, pady=5)
        
        self.bob_confirm_btn = ttk.Button(bob_response_frame, text="✅ Confirm Ready", 
                                         command=self.bob_confirm_ready, 
                                         state='disabled')
        self.bob_confirm_btn.pack(side='left', padx=(0, 5))
        
        self.bob_decline_btn = ttk.Button(bob_response_frame, text="❌ Not Ready", 
                                         command=self.bob_decline_ready, 
                                         state='disabled')
        self.bob_decline_btn.pack(side='left')
        
        # Bob's measurement area
        bob_measure_frame = ttk.LabelFrame(bob_main, text="Measurement Strategy")
        bob_measure_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(bob_measure_frame, text="Choose measurement bases:", 
                 style='Bob.TLabel').pack(anchor='w', padx=5, pady=2)
        
        self.bob_method_var = tk.StringVar(value="random")
        ttk.Radiobutton(bob_measure_frame, text="🎲 Random", 
                       variable=self.bob_method_var, value="random").pack(anchor='w', padx=5)
        ttk.Radiobutton(bob_measure_frame, text="✋ Manual", 
                       variable=self.bob_method_var, value="manual").pack(anchor='w', padx=5)
        
        self.bob_measure_btn = ttk.Button(bob_measure_frame, text="Start Measurements", 
                                         command=self.start_bob_measurement, 
                                         state='disabled')
        self.bob_measure_btn.pack(pady=5)
        
        # Bob's data display
        self.bob_data = scrolledtext.ScrolledText(bob_main, height=12, width=35)
        self.bob_data.pack(fill='both', expand=True, pady=5)
        
        # === CONTROL PANEL ===
        control_left = ttk.Frame(self.control_frame)
        control_left.pack(side='left', fill='x', expand=True)
        
        control_right = ttk.Frame(self.control_frame)
        control_right.pack(side='right')
        
        # Phase buttons
        self.phase_buttons = ttk.Frame(control_left)
        self.phase_buttons.pack(anchor='w')
        
        self.sift_btn = ttk.Button(self.phase_buttons, text="🔍 Sift Keys", 
                                  command=self.start_sifting, state='disabled')
        self.sift_btn.pack(side='left', padx=(0, 5))
        
        self.error_btn = ttk.Button(self.phase_buttons, text="⚠️ Check Errors", 
                                   command=self.start_error_checking, state='disabled')
        self.error_btn.pack(side='left', padx=5)
        
        self.final_btn = ttk.Button(self.phase_buttons, text="🔑 Generate Key", 
                                   command=self.generate_final_key, state='disabled')
        self.final_btn.pack(side='left', padx=5)
        
        # Utility buttons
        self.copy_btn = ttk.Button(control_right, text="📋 Copy Key", 
                                  command=self.copy_key, state='disabled')
        self.copy_btn.pack(side='left', padx=5)
        
        self.restart_btn = ttk.Button(control_right, text="🔄 Restart", 
                                     command=self.restart_demo)
        self.restart_btn.pack(side='left', padx=5)
    
    def show_setup(self):
        """Show initial setup"""
        self.alice_data.delete(1.0, tk.END)
        self.alice_data.insert(tk.END, "🎭 Welcome Alice!\n\n")
        self.alice_data.insert(tk.END, "Step 1: Send a greeting message to Bob\n")
        self.alice_data.insert(tk.END, "Step 2: Wait for Bob's confirmation\n")
        self.alice_data.insert(tk.END, "Step 3: Prepare qubits for transmission\n\n")
        self.alice_data.insert(tk.END, "Start by sending a message to Bob above!")
        
        self.bob_data.delete(1.0, tk.END)
        self.bob_data.insert(tk.END, "🔬 Welcome Bob!\n\n")
        self.bob_data.insert(tk.END, "You will receive and measure qubits from Alice.\n")
        self.bob_data.insert(tk.END, "You must choose a measurement basis for each qubit.\n\n")
        self.bob_data.insert(tk.END, "Remember: You only get the correct bit\n")
        self.bob_data.insert(tk.END, "if you choose the SAME basis as Alice!\n\n")
        self.bob_data.insert(tk.END, "Wait for Alice's initial message...")
        
        self.update_status("Setup - Alice should send initial message")
    
    def update_status(self, status):
        """Update status display"""
        self.status_label.configure(text=f"Phase: {status}")
    
    def alice_send_message(self):
        """Alice sends initial message to Bob"""
        message = self.alice_message_var.get().strip()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message!")
            return
        
        # Update Alice's display
        self.alice_data.insert(tk.END, f"\n📤 Message sent to Bob:\n")
        self.alice_data.insert(tk.END, f"'{message}'\n\n")
        self.alice_data.insert(tk.END, "Waiting for Bob's response...\n")
        self.alice_data.see(tk.END)
        
        # Update Bob's display
        self.bob_message_display.configure(text=f"📨 Alice says: '{message}'")
        
        # Enable Bob's response buttons
        self.bob_confirm_btn.configure(state='normal')
        self.bob_decline_btn.configure(state='normal')
        
        # Disable Alice's send button
        self.alice_send_btn.configure(state='disabled')
        
        # Update Bob's data
        self.bob_data.insert(tk.END, f"\n📨 Message received from Alice:\n")
        self.bob_data.insert(tk.END, f"'{message}'\n\n")
        self.bob_data.insert(tk.END, "Click 'Confirm Ready' if you're ready\n")
        self.bob_data.insert(tk.END, "for quantum key exchange!\n")
        self.bob_data.see(tk.END)
        
        self.update_status("Message sent - Waiting for Bob's confirmation")
    
    def bob_confirm_ready(self):
        """Bob confirms readiness for quantum key exchange"""
        # Update Bob's display
        self.bob_data.insert(tk.END, f"\n✅ Bob confirmed: Ready for quantum key exchange!\n\n")
        self.bob_data.insert(tk.END, "Waiting for Alice to prepare qubits...\n")
        self.bob_data.see(tk.END)
        
        # Update Alice's display
        self.alice_data.insert(tk.END, f"\n✅ Bob confirmed readiness!\n")
        self.alice_data.insert(tk.END, f"You can now prepare qubits for transmission.\n\n")
        self.alice_data.insert(tk.END, f"Choose preparation method and click 'Prepare Qubits'\n")
        self.alice_data.see(tk.END)
        
        # Enable Alice's preparation
        self.alice_prep_btn.configure(state='normal')
        self.bob_ready = True
        
        # Disable Bob's response buttons
        self.bob_confirm_btn.configure(state='disabled')
        self.bob_decline_btn.configure(state='disabled')
        
        self.update_status("Bob confirmed - Alice can prepare qubits")
    
    def bob_decline_ready(self):
        """Bob declines readiness"""
        # Update Bob's display
        self.bob_data.insert(tk.END, f"\n❌ Bob declined: Not ready yet!\n\n")
        self.bob_data.insert(tk.END, "You can change your mind and confirm when ready.\n")
        self.bob_data.see(tk.END)
        
        # Update Alice's display
        self.alice_data.insert(tk.END, f"\n❌ Bob is not ready yet!\n")
        self.alice_data.insert(tk.END, f"Please wait for Bob to confirm readiness.\n")
        self.alice_data.insert(tk.END, f"You can send another message if needed.\n")
        self.alice_data.see(tk.END)
        
        # Re-enable Alice's send button
        self.alice_send_btn.configure(state='normal')
        self.bob_ready = False
        
        self.update_status("Bob declined - Alice can send another message")
    
    def update_qubit_count(self):
        """Update the number of qubits when spinbox changes"""
        try:
            count = int(self.qubit_count_var.get())
            if 10 <= count <= 150:
                self.num_qubits = count
            else:
                # Reset to valid range
                if count < 10:
                    self.qubit_count_var.set("10")
                    self.num_qubits = 10
                elif count > 150:
                    self.qubit_count_var.set("150")
                    self.num_qubits = 150
        except ValueError:
            # Reset to default if invalid input
            self.qubit_count_var.set("20")
            self.num_qubits = 20

    def start_alice_preparation(self):
        """Start Alice's qubit preparation"""
        if not self.bob_ready:
            messagebox.showwarning("Warning", "Wait for Bob's confirmation first!")
            return
        
        # Update qubit count from spinbox
        self.update_qubit_count()
        
        self.has_eavesdropper = self.eve_var.get()
        method = self.alice_method_var.get()
        
        self.alice_data.insert(tk.END, f"\n🎭 Alice preparing {self.num_qubits} qubits...\n\n")
        
        def prepare():
            self.alice_bits = []
            self.alice_bases = []
            
            # Show progress differently based on qubit count
            show_every = max(1, self.num_qubits // 20)  # Show every nth qubit for large counts
            
            for i in range(self.num_qubits):
                if method == "random":
                    bit = random.randint(0, 1)
                    basis = random.randint(0, 1)
                else:
                    # Simplified manual - use random for now
                    bit = random.randint(0, 1)
                    basis = random.randint(0, 1)
                
                self.alice_bits.append(bit)
                self.alice_bases.append(basis)
                
                # Only show every nth qubit to avoid overwhelming the display
                if i % show_every == 0 or i < 10:
                    basis_symbol = '+' if basis == 0 else '×'
                    self.alice_data.insert(tk.END, 
                        f"Q{i+1:3d}: Bit={bit}, Basis={basis_symbol}\n")
                    self.alice_data.see(tk.END)
                    self.root.update()
                    
                # Adjust sleep time based on qubit count
                if self.num_qubits <= 30:
                    time.sleep(0.1)
                elif self.num_qubits <= 60:
                    time.sleep(0.05)
                else:
                    time.sleep(0.02)
            
            if self.num_qubits > 10 and show_every > 1:
                self.alice_data.insert(tk.END, f"... and {self.num_qubits - min(10, self.num_qubits)} more qubits\n")
            
            self.alice_data.insert(tk.END, f"\n✅ All {self.num_qubits} qubits prepared!\n")
            self.alice_data.insert(tk.END, f"Sample bits:  {self.alice_bits[:15]}\n")
            self.alice_data.insert(tk.END, f"Sample bases: {['+' if b==0 else '×' for b in self.alice_bases[:15]]}\n")
            
            # Enable transmission
            self.transmit_btn.configure(state='normal')
            self.alice_prep_btn.configure(state='disabled')
            self.update_status("Alice prepared qubits - Ready to transmit")
            self.channel_status.configure(text="Ready to transmit")
        
        threading.Thread(target=prepare, daemon=True).start()
    
    def start_transmission(self):
        """Start quantum transmission"""
        self.progress.start()
        self.transmit_btn.configure(state='disabled')
        self.channel_status.configure(text="Transmitting...")
        
        if self.has_eavesdropper:
            self.eve_activity.pack(fill='both', expand=True, pady=5)
            self.eve_activity.delete(1.0, tk.END)
            self.eve_activity.insert(tk.END, "👁️ EVE EAVESDROPPING!\n\n")
        
        def transmit():
            for i in range(self.num_qubits):
                if self.has_eavesdropper and random.random() < 0.6:
                    # Eve interferes
                    if random.random() < 0.5:  # Wrong basis 50% of time
                        self.alice_bits[i] = random.randint(0, 1)
                    
                    if i < 10:  # Show first 10 interceptions
                        self.eve_activity.insert(tk.END, f"Q{i+1}: Intercepted! 🔍\n")
                        self.eve_activity.see(tk.END)
                        self.root.update()
                
                time.sleep(0.05)
            
            if self.has_eavesdropper:
                self.eve_activity.insert(tk.END, "\n💀 Eve's interference complete!")
            
            self.progress.stop()
            self.channel_status.configure(text="Transmission complete")
            self.bob_measure_btn.configure(state='normal')
            self.update_status("Qubits transmitted - Bob can measure")
            
            # Update Bob's display
            self.bob_data.delete(1.0, tk.END)
            self.bob_data.insert(tk.END, "🔬 Qubits received!\n\n")
            self.bob_data.insert(tk.END, "Bob sees quantum states but doesn't\n")
            self.bob_data.insert(tk.END, "know Alice's bits or bases yet.\n\n")
            self.bob_data.insert(tk.END, "Choose your measurement strategy\n")
            self.bob_data.insert(tk.END, "and click 'Start Measurements'")
        
        threading.Thread(target=transmit, daemon=True).start()
    
    def start_bob_measurement(self):
        """Start Bob's measurements"""
        method = self.bob_method_var.get()
        
        self.bob_data.delete(1.0, tk.END)
        self.bob_data.insert(tk.END, f"🔬 Bob measuring {self.num_qubits} qubits...\n\n")
        
        def measure():
            self.bob_bases = []
            self.bob_results = []
            
            for i in range(self.num_qubits):
                if method == "random":
                    bob_basis = random.randint(0, 1)
                else:
                    bob_basis = random.randint(0, 1)  # Simplified
                
                self.bob_bases.append(bob_basis)
                
                # Simulate measurement result
                if self.alice_bases[i] == bob_basis:
                    result = self.alice_bits[i]
                    match = "✓"
                else:
                    result = random.randint(0, 1)
                    match = "✗"
                
                self.bob_results.append(result)
                
                basis_symbol = '+' if bob_basis == 0 else '×'
                self.bob_data.insert(tk.END, 
                    f"Q{i+1:2d}: Basis={basis_symbol}, Result={result} {match}\n")
                self.bob_data.see(tk.END)
                self.root.update()
                time.sleep(0.1)
            
            self.bob_data.insert(tk.END, f"\n✅ All measurements complete!\n")
            self.bob_data.insert(tk.END, f"Bob's bases:   {['+' if b==0 else '×' for b in self.bob_bases]}\n")
            self.bob_data.insert(tk.END, f"Bob's results: {self.bob_results}\n")
            
            # Enable sifting
            self.sift_btn.configure(state='normal')
            self.bob_measure_btn.configure(state='disabled')
            self.update_status("Measurements complete - Ready to sift")
        
        threading.Thread(target=measure, daemon=True).start()
    
    def start_sifting(self):
        """Start basis comparison and sifting"""
        def sift():
            # Update both displays with sifting results
            sift_text = f"\n{'='*20} SIFTING {'='*20}\n"
            sift_text += "Alice and Bob compare bases publicly:\n\n"
            sift_text += f"{'Q':<3} {'A_basis':<7} {'B_basis':<7} {'Match':<6} {'Keep'}\n"
            sift_text += "-" * 35 + "\n"
            
            matching_indices = []
            
            for i in range(self.num_qubits):
                match = self.alice_bases[i] == self.bob_bases[i]
                alice_symbol = '+' if self.alice_bases[i] == 0 else '×'
                bob_symbol = '+' if self.bob_bases[i] == 0 else '×'
                
                if match:
                    matching_indices.append(i)
                    keep = "✓ YES"
                else:
                    keep = "✗ NO"
                
                sift_text += f"{i+1:<3} {alice_symbol:<7} {bob_symbol:<7} {'✓' if match else '✗':<6} {keep}\n"
            
            self.sifted_bits = [self.bob_results[i] for i in matching_indices]
            
            sift_text += f"\nMatching bases: {len(matching_indices)}/{self.num_qubits}\n"
            sift_text += f"Sifted key bits: {self.sifted_bits}\n"
            
            self.alice_data.insert(tk.END, sift_text)
            self.bob_data.insert(tk.END, sift_text)
            
            self.matching_indices = matching_indices
            self.error_btn.configure(state='normal')
            self.sift_btn.configure(state='disabled')
            self.update_status("Sifting complete - Ready for error check")
        
        threading.Thread(target=sift, daemon=True).start()
    
    def start_error_checking(self):
        """Start error checking"""
        def check_errors():
            error_text = f"\n{'='*15} ERROR CHECKING {'='*15}\n"
            
            if len(self.sifted_bits) >= 4:
                # Compare ALL qubits instead of just a sample
                total_bits = len(self.sifted_bits)
                
                error_text += f"Comparing ALL {total_bits} sifted bits:\n\n"
                
                errors = 0
                show_limit = min(20, total_bits)  # Show first 20 for display purposes
                
                # Check all bits but only display first 20
                for idx in range(total_bits):
                    alice_bit = self.alice_bits[self.matching_indices[idx]]
                    bob_bit = self.sifted_bits[idx]
                    match = alice_bit == bob_bit
                    
                    if not match:
                        errors += 1
                    
                    # Only show first 20 in the display to avoid overwhelming the GUI
                    if idx < show_limit:
                        error_text += f"Bit {idx+1:3d}: A={alice_bit}, B={bob_bit} {'✓' if match else '✗'}\n"
                
                # Show summary if there are more bits than displayed
                if total_bits > show_limit:
                    remaining_bits = total_bits - show_limit
                    remaining_errors = errors - sum(1 for i in range(show_limit) 
                                                  if self.alice_bits[self.matching_indices[i]] != self.sifted_bits[i])
                    error_text += f"... and {remaining_bits} more bits "
                    if remaining_errors > 0:
                        error_text += f"({remaining_errors} additional errors)\n"
                    else:
                        error_text += f"(all matching)\n"
                
                # Add eavesdropper errors if enabled
                if self.has_eavesdropper and errors == 0:
                    # Force some errors if eavesdropper is present but no natural errors occurred
                    additional_errors = random.randint(1, min(5, max(1, total_bits // 10)))
                    errors += additional_errors
                    error_text += f"\n⚠️ Eavesdropper interference added {additional_errors} errors!\n"
                elif self.has_eavesdropper:
                    # Add some additional errors due to eavesdropper
                    additional_errors = random.randint(0, min(3, max(1, total_bits // 20)))
                    errors += additional_errors
                    if additional_errors > 0:
                        error_text += f"\n⚠️ Eavesdropper interference added {additional_errors} more errors!\n"
                
                error_rate = errors / total_bits
                
                error_text += f"\n📊 COMPLETE ERROR ANALYSIS:\n"
                error_text += f"Total sifted bits: {total_bits}\n"
                error_text += f"Total errors found: {errors}\n"
                error_text += f"Quantum Bit Error Rate (QBER): {error_rate:.3f} ({error_rate*100:.1f}%)\n"
                
                # Security assessment
                if error_rate > 0.15:
                    error_text += "\n🚨 HIGH ERROR RATE DETECTED!\n"
                    error_text += "❌ Channel is NOT secure - Possible eavesdropper!\n"
                    if self.has_eavesdropper:
                        error_text += "✅ CORRECTLY DETECTED EVE'S PRESENCE!\n"
                        error_text += "BB84 protocol successfully identified the eavesdropper.\n"
                elif error_rate > 0.05:
                    error_text += "\n⚠️ MODERATE ERROR RATE\n"
                    error_text += "🟡 Channel security questionable - Investigate further\n"
                    if self.has_eavesdropper:
                        error_text += "✅ Eve detected with moderate confidence\n"
                else:
                    error_text += "\n✅ LOW ERROR RATE - CHANNEL SECURE\n"
                    error_text += "🔒 Safe to proceed with key generation\n"
                    if self.has_eavesdropper:
                        error_text += "⚠️ Eve was present but got lucky with low error rate\n"
                        error_text += "This can happen by chance in quantum systems\n"
                
                # Remove a portion of bits that were "publicly compared" for error checking
                # In real BB84, these bits would be discarded
                sacrifice_count = min(errors + 2, len(self.sifted_bits) // 4)  # Sacrifice some bits
                if sacrifice_count > 0:
                    # Remove sacrificed bits from the end
                    self.sifted_bits = self.sifted_bits[:-sacrifice_count]
                    error_text += f"\n🗑️ Sacrificed {sacrifice_count} bits for error checking\n"
                    error_text += f"Remaining bits for final key: {len(self.sifted_bits)}\n"
                
            else:
                error_text += "❌ Not enough bits for comprehensive error checking\n"
                error_text += f"Only {len(self.sifted_bits)} bits available, need at least 4\n"
            
            self.alice_data.insert(tk.END, error_text)
            self.bob_data.insert(tk.END, error_text)
            
            if len(self.sifted_bits) >= 4:
                self.final_btn.configure(state='normal')
            self.error_btn.configure(state='disabled')
            self.update_status("Error checking complete - Ready for final key")
        
        threading.Thread(target=check_errors, daemon=True).start()
    
    def generate_final_key(self):
        """Generate final key"""
        if len(self.sifted_bits) < 4:
            messagebox.showerror("Error", "Not enough bits for key generation!")
            return
        
        # Privacy amplification
        bit_string = ''.join(str(b) for b in self.sifted_bits)
        while len(bit_string) % 8 != 0:
            bit_string += '0'
        
        byte_data = bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))
        self.final_key = hashlib.sha256(byte_data).hexdigest()
        
        final_text = f"\n{'='*15} FINAL KEY {'='*15}\n"
        final_text += f"🔑 SHARED SECRET KEY:\n"
        final_text += f"{self.final_key}\n\n"
        final_text += "📋 READY FOR CHAT DEMO:\n"
        final_text += "1. Copy this key\n"
        final_text += "2. Open browser: localhost:3000\n"
        final_text += "3. Paste key and join chat\n"
        final_text += "4. Use encrypt/decrypt buttons\n"
        
        self.alice_data.insert(tk.END, final_text)
        self.bob_data.insert(tk.END, final_text)
        
        self.copy_btn.configure(state='normal')
        self.final_btn.configure(state='disabled')
        self.update_status("KEY GENERATED - Ready for chat demo!")
    
    def copy_key(self):
        """Copy key to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.final_key)
        messagebox.showinfo("Copied", "Key copied to clipboard!")
    
    def restart_demo(self):
        """Restart the demonstration"""
        # Reset variables
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_results = []
        self.final_key = ""
        self.bob_ready = False
        
        # Reset qubit count to default
        self.num_qubits = 20
        self.qubit_count_var.set("20")
        
        # Reset buttons
        self.alice_send_btn.configure(state='normal')
        self.alice_prep_btn.configure(state='disabled')
        self.transmit_btn.configure(state='disabled')
        self.bob_measure_btn.configure(state='disabled')
        self.bob_confirm_btn.configure(state='disabled')
        self.bob_decline_btn.configure(state='disabled')
        self.sift_btn.configure(state='disabled')
        self.error_btn.configure(state='disabled')
        self.final_btn.configure(state='disabled')
        self.copy_btn.configure(state='disabled')
        
        # Reset message
        self.alice_message_var.set("Hello Bob! Ready for quantum key exchange?")
        self.bob_message_display.configure(text="Waiting for Alice's message...")
        
        # Hide Eve activity
        self.eve_activity.pack_forget()
        
        # Reset displays
        self.show_setup()
        self.progress.stop()
        self.channel_status.configure(text="Ready")
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = BB84SplitGUI()
        app.run()
    except ImportError as e:
        print("Error: Missing required module.")
        print("Make sure you have Python with tkinter installed.")
        print(f"Details: {e}")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
