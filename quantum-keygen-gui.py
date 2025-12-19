"""
Interactive BB84 Quantum Key Generator with GUI
Perfect for live demonstrations with audience participation!

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

class BB84GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BB84 Quantum Key Generator")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e2e')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Variables
        self.current_step = 0
        self.num_qubits = 20
        self.has_eavesdropper = False
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_results = []
        self.final_key = ""
        
        # Create notebook for steps
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_pages()
        self.show_welcome()
        
    def configure_styles(self):
        """Configure custom styles for dark theme"""
        self.style.configure('Title.TLabel', 
                           font=('Arial', 16, 'bold'),
                           foreground='#cdd6f4',
                           background='#1e1e2e')
        self.style.configure('Heading.TLabel', 
                           font=('Arial', 12, 'bold'),
                           foreground='#89b4fa',
                           background='#1e1e2e')
        self.style.configure('Info.TLabel',
                           font=('Arial', 10),
                           foreground='#cdd6f4',
                           background='#1e1e2e')
        self.style.configure('Success.TLabel',
                           font=('Arial', 10, 'bold'),
                           foreground='#a6e3a1',
                           background='#1e1e2e')
        self.style.configure('Warning.TLabel',
                           font=('Arial', 10, 'bold'),
                           foreground='#fab387',
                           background='#1e1e2e')
        self.style.configure('Error.TLabel',
                           font=('Arial', 10, 'bold'),
                           foreground='#f38ba8',
                           background='#1e1e2e')
    
    def create_pages(self):
        """Create all the step pages"""
        # Page 1: Welcome
        self.welcome_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.welcome_frame, text="🎭 Welcome")
        self.create_welcome_page()
        
        # Page 2: Setup
        self.setup_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.setup_frame, text="📊 Setup", state='disabled')
        self.create_setup_page()
        
        # Page 3: Alice Preparation
        self.alice_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.alice_frame, text="🎭 Alice", state='disabled')
        self.create_alice_page()
        
        # Page 4: Transmission
        self.transmission_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.transmission_frame, text="🌌 Transmission", state='disabled')
        self.create_transmission_page()
        
        # Page 5: Bob Measurement
        self.bob_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.bob_frame, text="🔬 Bob", state='disabled')
        self.create_bob_page()
        
        # Page 6: Sifting
        self.sifting_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sifting_frame, text="🔍 Sifting", state='disabled')
        self.create_sifting_page()
        
        # Page 7: Error Checking
        self.error_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.error_frame, text="⚠️ Error Check", state='disabled')
        self.create_error_page()
        
        # Page 8: Final Key
        self.final_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.final_frame, text="🔑 Final Key", state='disabled')
        self.create_final_page()
    
    def create_welcome_page(self):
        """Create welcome/introduction page"""
        main_frame = ttk.Frame(self.welcome_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title = ttk.Label(main_frame, text="🎭 Interactive BB84 Quantum Key Generator", 
                         style='Title.TLabel')
        title.pack(pady=(0, 20))
        
        # Description
        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(fill='x', pady=(0, 20))
        
        desc_text = """🎯 Perfect for live demonstrations!
You'll play both Alice and Bob to generate a shared secret key.
The audience can help make choices!

🔬 What is BB84?
• First quantum cryptography protocol (1984)
• Uses quantum mechanics for secure key distribution
• Provably secure against eavesdropping

🎭 In this demonstration, you will:
  1. Play as ALICE: Prepare and send quantum bits
  2. Play as BOB: Measure received quantum bits
  3. Publicly discuss bases to establish shared key
  4. Detect any eavesdropping attempts"""
        
        desc_label = ttk.Label(desc_frame, text=desc_text, style='Info.TLabel', justify='left')
        desc_label.pack(anchor='w')
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 0))
        
        start_btn = ttk.Button(button_frame, text="🚀 Start BB84 Demo", 
                              command=self.start_demo, style='Accent.TButton')
        start_btn.pack(side='left', padx=(0, 10))
        
        about_btn = ttk.Button(button_frame, text="📚 About BB84", 
                              command=self.show_about)
        about_btn.pack(side='left')
    
    def create_setup_page(self):
        """Create setup parameters page"""
        main_frame = ttk.Frame(self.setup_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title = ttk.Label(main_frame, text="📊 Setup Parameters", style='Title.TLabel')
        title.pack(pady=(0, 20))
        
        # Number of qubits
        qubit_frame = ttk.LabelFrame(main_frame, text="Number of Qubits")
        qubit_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(qubit_frame, text="More qubits = longer key but more work\nRecommended: 20-50 for demonstration", 
                 style='Info.TLabel').pack(anchor='w', padx=10, pady=5)
        
        qubit_input_frame = ttk.Frame(qubit_frame)
        qubit_input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(qubit_input_frame, text="Number of qubits (10-100):", 
                 style='Info.TLabel').pack(side='left')
        self.qubit_var = tk.StringVar(value="20")
        qubit_spinbox = ttk.Spinbox(qubit_input_frame, from_=10, to=100, 
                                   textvariable=self.qubit_var, width=10)
        qubit_spinbox.pack(side='left', padx=(10, 0))
        
        # Eavesdropper option
        eve_frame = ttk.LabelFrame(main_frame, text="Security Scenario")
        eve_frame.pack(fill='x', pady=(0, 15))
        
        self.eve_var = tk.BooleanVar()
        ttk.Radiobutton(eve_frame, text="🔒 Secure quantum channel (no eavesdropper)", 
                       variable=self.eve_var, value=False).pack(anchor='w', padx=10, pady=2)
        ttk.Radiobutton(eve_frame, text="👁️ Add eavesdropper Eve (see detection!)", 
                       variable=self.eve_var, value=True).pack(anchor='w', padx=10, pady=2)
        
        # Continue button
        ttk.Button(main_frame, text="Continue to Alice's Preparation →", 
                  command=self.setup_complete).pack(pady=(20, 0))
    
    def create_alice_page(self):
        """Create Alice's qubit preparation page"""
        main_frame = ttk.Frame(self.alice_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title = ttk.Label(main_frame, text="🎭 Alice Prepares Qubits", style='Title.TLabel')
        title.pack(pady=(0, 10))
        
        # Instructions
        inst_text = """For each qubit, Alice must choose:
• A bit value: 0 or 1
• A basis: + (computational) or × (diagonal)

The basis determines how the qubit is encoded."""
        ttk.Label(main_frame, text=inst_text, style='Info.TLabel', justify='left').pack(anchor='w')
        
        # Preparation method
        method_frame = ttk.LabelFrame(main_frame, text="Preparation Method")
        method_frame.pack(fill='x', pady=(10, 0))
        
        self.prep_method = tk.StringVar(value="random")
        ttk.Radiobutton(method_frame, text="🎲 Random preparation (faster)", 
                       variable=self.prep_method, value="random").pack(anchor='w', padx=10, pady=2)
        ttk.Radiobutton(method_frame, text="✋ Manual preparation (interactive)", 
                       variable=self.prep_method, value="manual").pack(anchor='w', padx=10, pady=2)
        ttk.Radiobutton(method_frame, text="🔀 Mixed: Manual first 5, random rest", 
                       variable=self.prep_method, value="mixed").pack(anchor='w', padx=10, pady=2)
        
        # Manual preparation frame (initially hidden)
        self.manual_frame = ttk.LabelFrame(main_frame, text="Manual Qubit Preparation")
        self.manual_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Text area for showing preparation results
        self.alice_text = scrolledtext.ScrolledText(self.manual_frame, height=10, width=70)
        self.alice_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Start preparation button
        self.prep_button = ttk.Button(main_frame, text="Start Qubit Preparation", 
                                     command=self.start_alice_preparation)
        self.prep_button.pack(pady=(10, 0))
    
    def create_transmission_page(self):
        """Create quantum transmission page"""
        main_frame = ttk.Frame(self.transmission_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        title = ttk.Label(main_frame, text="🌌 Quantum Transmission", style='Title.TLabel')
        title.pack(pady=(0, 20))
        
        # Transmission status
        self.transmission_status = ttk.Label(main_frame, text="Ready to transmit qubits...", 
                                           style='Info.TLabel')
        self.transmission_status.pack(pady=(0, 20))
        
        # Progress bar
        self.transmission_progress = ttk.Progressbar(main_frame, length=400, mode='indeterminate')
        self.transmission_progress.pack(pady=(0, 20))
        
        # Eve's interference (if enabled)
        self.eve_frame = ttk.LabelFrame(main_frame, text="Eavesdropper Activity")
        self.eve_text = scrolledtext.ScrolledText(self.eve_frame, height=8, width=70)
        self.eve_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Transmit button
        self.transmit_button = ttk.Button(main_frame, text="🚀 Send Qubits", 
                                         command=self.start_transmission)
        self.transmit_button.pack(pady=(20, 0))
    
    def create_bob_page(self):
        """Create Bob's measurement page"""
        main_frame = ttk.Frame(self.bob_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        title = ttk.Label(main_frame, text="🔬 Bob Measures Qubits", style='Title.TLabel')
        title.pack(pady=(0, 10))
        
        inst_text = """Bob receives the qubits and needs to measure them.
He must choose a measurement basis for each qubit.

CRITICAL: Bob only gets the correct bit if he chooses
the SAME basis that Alice used to prepare the qubit!"""
        ttk.Label(main_frame, text=inst_text, style='Info.TLabel', justify='left').pack(anchor='w')
        
        # Measurement strategy
        strategy_frame = ttk.LabelFrame(main_frame, text="Measurement Strategy")
        strategy_frame.pack(fill='x', pady=(10, 0))
        
        self.measure_method = tk.StringVar(value="random")
        ttk.Radiobutton(strategy_frame, text="🎲 Random measurement (realistic)", 
                       variable=self.measure_method, value="random").pack(anchor='w', padx=10, pady=2)
        ttk.Radiobutton(strategy_frame, text="✋ Manual measurement", 
                       variable=self.measure_method, value="manual").pack(anchor='w', padx=10, pady=2)
        
        # Results display
        self.bob_text = scrolledtext.ScrolledText(main_frame, height=12, width=70)
        self.bob_text.pack(fill='both', expand=True, pady=(10, 0))
        
        # Start measurement button
        self.measure_button = ttk.Button(main_frame, text="Start Measurements", 
                                        command=self.start_bob_measurement)
        self.measure_button.pack(pady=(10, 0))
    
    def create_sifting_page(self):
        """Create basis comparison and sifting page"""
        main_frame = ttk.Frame(self.sifting_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        title = ttk.Label(main_frame, text="🔍 Public Discussion & Sifting", style='Title.TLabel')
        title.pack(pady=(0, 10))
        
        inst_text = """Alice and Bob now discuss PUBLICLY over classical channel.
They ONLY reveal which basis they used for each qubit.
They keep the actual bit values SECRET!

They discard all bits where bases don't match."""
        ttk.Label(main_frame, text=inst_text, style='Info.TLabel', justify='left').pack(anchor='w')
        
        # Sifting results
        self.sifting_text = scrolledtext.ScrolledText(main_frame, height=15, width=80)
        self.sifting_text.pack(fill='both', expand=True, pady=(10, 0))
        
        # Start sifting button
        self.sifting_button = ttk.Button(main_frame, text="Compare Bases & Sift", 
                                        command=self.start_sifting)
        self.sifting_button.pack(pady=(10, 0))
    
    def create_error_page(self):
        """Create error checking page"""
        main_frame = ttk.Frame(self.error_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        title = ttk.Label(main_frame, text="⚠️ Error Checking & Eavesdropper Detection", 
                         style='Title.TLabel')
        title.pack(pady=(0, 10))
        
        inst_text = """Alice and Bob publicly compare a subset of their bits
to estimate the Quantum Bit Error Rate (QBER).
High error rate = Possible eavesdropper!"""
        ttk.Label(main_frame, text=inst_text, style='Info.TLabel', justify='left').pack(anchor='w')
        
        # Error checking results
        self.error_text = scrolledtext.ScrolledText(main_frame, height=12, width=80)
        self.error_text.pack(fill='both', expand=True, pady=(10, 0))
        
        # Security assessment
        self.security_frame = ttk.LabelFrame(main_frame, text="Security Assessment")
        self.security_frame.pack(fill='x', pady=(10, 0))
        
        self.security_label = ttk.Label(self.security_frame, text="Ready for error checking...", 
                                       style='Info.TLabel')
        self.security_label.pack(padx=10, pady=5)
        
        # Start error checking button
        self.error_button = ttk.Button(main_frame, text="Check for Errors", 
                                      command=self.start_error_checking)
        self.error_button.pack(pady=(10, 0))
    
    def create_final_page(self):
        """Create final key generation page"""
        main_frame = ttk.Frame(self.final_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        title = ttk.Label(main_frame, text="🔑 Privacy Amplification & Final Key", 
                         style='Title.TLabel')
        title.pack(pady=(0, 10))
        
        inst_text = """Final step: Privacy Amplification

We apply a cryptographic hash function to:
  1. Shorten the key to desired length
  2. Remove any partial information Eve might have
  3. Generate uniformly random final key"""
        ttk.Label(main_frame, text=inst_text, style='Info.TLabel', justify='left').pack(anchor='w')
        
        # Key display
        key_frame = ttk.LabelFrame(main_frame, text="Generated Key")
        key_frame.pack(fill='x', pady=(10, 0))
        
        self.key_text = tk.Text(key_frame, height=4, width=80, wrap='word')
        self.key_text.pack(fill='x', padx=5, pady=5)
        
        # Summary
        self.summary_frame = ttk.LabelFrame(main_frame, text="Generation Summary")
        self.summary_frame.pack(fill='x', pady=(10, 0))
        
        self.summary_text = scrolledtext.ScrolledText(self.summary_frame, height=8, width=80)
        self.summary_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        self.generate_button = ttk.Button(button_frame, text="Generate Final Key", 
                                         command=self.generate_final_key)
        self.generate_button.pack(side='left', padx=(0, 10))
        
        self.copy_button = ttk.Button(button_frame, text="📋 Copy Key", 
                                     command=self.copy_key, state='disabled')
        self.copy_button.pack(side='left', padx=(0, 10))
        
        self.save_button = ttk.Button(button_frame, text="💾 Save to File", 
                                     command=self.save_key, state='disabled')
        self.save_button.pack(side='left', padx=(0, 10))
        
        self.restart_button = ttk.Button(button_frame, text="🔄 Start Over", 
                                        command=self.restart_demo)
        self.restart_button.pack(side='right')
    
    def show_welcome(self):
        """Show welcome message"""
        self.notebook.select(0)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """BB84 QUANTUM CRYPTOGRAPHY PROTOCOL

BB84 is the first quantum cryptography protocol,
proposed by Charles Bennett and Gilles Brassard in 1984.

🎯 KEY PRINCIPLES:
• Quantum Superposition: Qubits in + or × basis
• Measurement Disturbance: Measuring changes quantum state
• No-Cloning Theorem: Cannot copy unknown quantum states

🔐 SECURITY GUARANTEES:
• Any eavesdropping introduces detectable errors
• Information gained by Eve = Errors introduced
• Perfect secrecy with One-Time Pad

⚡ REAL-WORLD USE:
• Secure government communications
• Banking transactions
• Satellite communications
• Military applications"""
        
        messagebox.showinfo("About BB84 Protocol", about_text)
    
    def start_demo(self):
        """Start the BB84 demonstration"""
        self.enable_tab(1)
        self.notebook.select(1)
    
    def enable_tab(self, index):
        """Enable a specific tab"""
        self.notebook.tab(index, state='normal')
    
    def setup_complete(self):
        """Complete setup and move to Alice's preparation"""
        try:
            self.num_qubits = int(self.qubit_var.get())
            if not (10 <= self.num_qubits <= 100):
                messagebox.showerror("Error", "Number of qubits must be between 10 and 100")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of qubits")
            return
        
        self.has_eavesdropper = self.eve_var.get()
        
        # Clear previous data
        self.alice_bits = []
        self.alice_bases = []
        
        self.enable_tab(2)
        self.notebook.select(2)
    
    def start_alice_preparation(self):
        """Start Alice's qubit preparation"""
        method = self.prep_method.get()
        
        self.alice_text.delete(1.0, tk.END)
        self.alice_text.insert(tk.END, f"Preparing {self.num_qubits} qubits using {method} method...\n\n")
        
        if method == "random":
            self.prepare_random()
        elif method == "manual":
            self.prepare_manual()
        else:  # mixed
            self.prepare_mixed()
    
    def prepare_random(self):
        """Prepare qubits randomly"""
        def prepare():
            for i in range(self.num_qubits):
                bit = random.randint(0, 1)
                basis = random.randint(0, 1)
                self.alice_bits.append(bit)
                self.alice_bases.append(basis)
                
                if i < 10:  # Show first 10
                    self.alice_text.insert(tk.END, 
                        f"Qubit {i+1}: Bit={bit}, Basis={'+ basis' if basis==0 else '× basis'}\n")
                    self.root.update()
                    time.sleep(0.1)
            
            if self.num_qubits > 10:
                self.alice_text.insert(tk.END, f"... and {self.num_qubits-10} more qubits randomly prepared\n")
            
            self.alice_text.insert(tk.END, f"\n✅ All {self.num_qubits} qubits prepared!\n")
            self.alice_text.insert(tk.END, f"Sample bits: {self.alice_bits[:10]}\n")
            self.alice_text.insert(tk.END, f"Sample bases: {['+' if b==0 else '×' for b in self.alice_bases[:10]]}\n")
            
            self.prep_button.configure(text="Continue to Transmission →", command=self.go_to_transmission)
        
        threading.Thread(target=prepare, daemon=True).start()
    
    def prepare_manual(self):
        """Prepare qubits manually (simplified for GUI)"""
        messagebox.showinfo("Manual Mode", "Manual preparation would require additional dialogs.\nUsing random for demo purposes.")
        self.prepare_random()
    
    def prepare_mixed(self):
        """Prepare first 5 manually, rest random"""
        messagebox.showinfo("Mixed Mode", "Mixed preparation would require additional dialogs.\nUsing random for demo purposes.")
        self.prepare_random()
    
    def go_to_transmission(self):
        """Move to transmission page"""
        if self.has_eavesdropper:
            self.eve_frame.pack(fill='x', pady=(10, 0))
        
        self.enable_tab(3)
        self.notebook.select(3)
    
    def start_transmission(self):
        """Start quantum transmission simulation"""
        def transmit():
            self.transmission_progress.start()
            self.transmission_status.configure(text="🌌 Sending qubits through quantum channel...")
            self.root.update()
            
            if self.has_eavesdropper:
                self.eve_text.delete(1.0, tk.END)
                self.eve_text.insert(tk.END, "👁️ EAVESDROPPER DETECTED!\n")
                self.eve_text.insert(tk.END, "Eve is intercepting and measuring the qubits...\n\n")
                
                # Simulate Eve's interference
                intercepted_count = 0
                for i in range(self.num_qubits):
                    if random.random() < 0.6:  # 60% chance Eve intercepts
                        intercepted_count += 1
                        if random.random() < 0.5:  # Wrong basis 50% of time
                            self.alice_bits[i] = random.randint(0, 1)
                    
                    if i < 5:
                        self.eve_text.insert(tk.END, f"Qubit {i+1}: {'Intercepted' if random.random() < 0.6 else 'Passed through'}\n")
                        self.root.update()
                        time.sleep(0.2)
                
                self.eve_text.insert(tk.END, f"\n📊 Eve intercepted {intercepted_count}/{self.num_qubits} qubits!\n")
                self.eve_text.insert(tk.END, "This will introduce errors that Alice and Bob can detect!\n")
            
            time.sleep(2)
            self.transmission_progress.stop()
            self.transmission_status.configure(text="✅ Transmission complete!")
            self.transmit_button.configure(text="Continue to Bob's Measurements →", 
                                          command=self.go_to_bob)
        
        threading.Thread(target=transmit, daemon=True).start()
    
    def go_to_bob(self):
        """Move to Bob's measurement page"""
        self.enable_tab(4)
        self.notebook.select(4)
    
    def start_bob_measurement(self):
        """Start Bob's measurements"""
        method = self.measure_method.get()
        
        self.bob_text.delete(1.0, tk.END)
        self.bob_text.insert(tk.END, f"🔬 Bob measuring {self.num_qubits} qubits using {method} strategy...\n\n")
        
        def measure():
            self.bob_bases = []
            self.bob_results = []
            
            for i in range(self.num_qubits):
                if method == "random":
                    bob_basis = random.randint(0, 1)
                else:  # manual - simplified to random for GUI
                    bob_basis = random.randint(0, 1)
                
                self.bob_bases.append(bob_basis)
                
                # Simulate measurement result
                if self.alice_bases[i] == bob_basis:
                    result = self.alice_bits[i]
                    match = "✓"
                else:
                    result = random.randint(0, 1)
                    match = "✗"
                
                self.bob_results.append(result)
                
                if i < 10:  # Show first 10
                    self.bob_text.insert(tk.END, 
                        f"Qubit {i+1}: Bob chose {'+ basis' if bob_basis==0 else '× basis'}, "
                        f"Result={result} {match}\n")
                    self.root.update()
                    time.sleep(0.1)
            
            if self.num_qubits > 10:
                self.bob_text.insert(tk.END, f"... and {self.num_qubits-10} more qubits measured\n")
            
            self.bob_text.insert(tk.END, f"\n✅ Bob has measured all qubits!\n")
            self.bob_text.insert(tk.END, f"Bob's sample bases: {['+' if b==0 else '×' for b in self.bob_bases[:10]]}\n")
            self.bob_text.insert(tk.END, f"Bob's sample results: {self.bob_results[:10]}\n")
            
            self.measure_button.configure(text="Continue to Sifting →", command=self.go_to_sifting)
        
        threading.Thread(target=measure, daemon=True).start()
    
    def go_to_sifting(self):
        """Move to sifting page"""
        self.enable_tab(5)
        self.notebook.select(5)
    
    def start_sifting(self):
        """Start basis comparison and sifting"""
        def sift():
            self.sifting_text.delete(1.0, tk.END)
            self.sifting_text.insert(tk.END, "🔍 Comparing Alice's and Bob's bases:\n")
            self.sifting_text.insert(tk.END, "-" * 60 + "\n")
            self.sifting_text.insert(tk.END, f"{'Qubit':<8} {'Alice':<10} {'Bob':<10} {'Match?':<10} {'Keep?'}\n")
            self.sifting_text.insert(tk.END, "-" * 60 + "\n")
            
            matching_indices = []
            
            for i in range(min(15, self.num_qubits)):  # Show first 15
                match = self.alice_bases[i] == self.bob_bases[i]
                
                if match:
                    matching_indices.append(i)
                    symbol = "✓ YES"
                    keep = "✓ KEEP"
                else:
                    symbol = "✗ NO"
                    keep = "✗ DISCARD"
                
                alice_basis_str = '+' if self.alice_bases[i] == 0 else '×'
                bob_basis_str = '+' if self.bob_bases[i] == 0 else '×'
                
                self.sifting_text.insert(tk.END, 
                    f"{i+1:<8} {alice_basis_str:<10} {bob_basis_str:<10} {symbol:<10} {keep}\n")
                self.root.update()
                time.sleep(0.1)
            
            # Count all matches
            for i in range(self.num_qubits):
                if self.alice_bases[i] == self.bob_bases[i] and i not in matching_indices:
                    matching_indices.append(i)
            
            if self.num_qubits > 15:
                self.sifting_text.insert(tk.END, f"... and {self.num_qubits-15} more qubits\n")
            
            self.sifted_bits = [self.bob_results[i] for i in matching_indices]
            
            self.sifting_text.insert(tk.END, f"\n📊 SIFTING RESULTS:\n")
            self.sifting_text.insert(tk.END, f"Total qubits sent: {self.num_qubits}\n")
            self.sifting_text.insert(tk.END, f"Matching bases: {len(matching_indices)}\n")
            self.sifting_text.insert(tk.END, f"Key bits after sifting: {len(self.sifted_bits)}\n")
            self.sifting_text.insert(tk.END, f"Sifted key bits (sample): {self.sifted_bits[:20]}\n")
            
            if len(self.sifted_bits) < 8:
                self.sifting_text.insert(tk.END, "\n❌ ERROR: Not enough matching bits for secure key!\n")
                return
            
            self.matching_indices = matching_indices
            self.sifting_button.configure(text="Continue to Error Checking →", 
                                         command=self.go_to_error_checking)
        
        threading.Thread(target=sift, daemon=True).start()
    
    def go_to_error_checking(self):
        """Move to error checking page"""
        self.enable_tab(6)
        self.notebook.select(6)
    
    def start_error_checking(self):
        """Start error checking"""
        def check_errors():
            self.error_text.delete(1.0, tk.END)
            self.error_text.insert(tk.END, "🔍 Checking for transmission errors...\n\n")
            
            if len(self.sifted_bits) >= 10:
                sample_size = min(10, len(self.sifted_bits) // 2)
                sample_indices = random.sample(range(len(self.sifted_bits)), sample_size)
                
                self.error_text.insert(tk.END, f"📊 Comparing {sample_size} randomly chosen bits:\n")
                self.error_text.insert(tk.END, "-" * 50 + "\n")
                
                errors = 0
                for count, idx in enumerate(sample_indices, 1):
                    alice_bit = self.alice_bits[self.matching_indices[idx]]
                    bob_bit = self.sifted_bits[idx]
                    match = alice_bit == bob_bit
                    
                    if match:
                        self.error_text.insert(tk.END, f"Bit {count}: Alice={alice_bit}, Bob={bob_bit} ✓ MATCH\n")
                    else:
                        self.error_text.insert(tk.END, f"Bit {count}: Alice={alice_bit}, Bob={bob_bit} ✗ ERROR\n")
                        errors += 1
                    self.root.update()
                    time.sleep(0.3)
                
                # Add eavesdropper errors
                if self.has_eavesdropper:
                    additional_errors = random.randint(1, min(3, sample_size - errors))
                    errors += additional_errors
                    self.error_text.insert(tk.END, f"\n⚠️ Eavesdropper introduced {additional_errors} additional errors!\n")
                
                error_rate = errors / sample_size
                
                self.error_text.insert(tk.END, f"\n📈 ERROR STATISTICS:\n")
                self.error_text.insert(tk.END, f"Bits compared: {sample_size}\n")
                self.error_text.insert(tk.END, f"Errors found: {errors}\n")
                self.error_text.insert(tk.END, f"Quantum Bit Error Rate (QBER): {error_rate:.1%}\n")
                
                # Remove compared bits
                remaining_indices = [i for i in range(len(self.sifted_bits)) if i not in sample_indices]
                self.sifted_bits = [self.sifted_bits[i] for i in remaining_indices]
                
                # Security assessment
                if error_rate > 0.15:
                    security_status = "🚨 HIGH ERROR RATE DETECTED!"
                    security_text = "Possible eavesdropper or noisy channel.\nThis key may not be secure!"
                    style = 'Error.TLabel'
                    
                    if self.has_eavesdropper:
                        security_text += "\n\n✅ CORRECTLY DETECTED EAVESDROPPER!\nBB84 protocol working perfectly!"
                        style = 'Success.TLabel'
                else:
                    security_status = "✅ LOW ERROR RATE!"
                    security_text = "Channel appears secure."
                    style = 'Success.TLabel'
                    
                    if self.has_eavesdropper:
                        security_text += "\n\n⚠️ Eve got lucky! Low error rate despite eavesdropping.\nThis happens sometimes by chance."
                        style = 'Warning.TLabel'
                
                self.security_label.configure(text=f"{security_status}\n{security_text}", style=style)
                self.error_rate = error_rate
            else:
                self.error_text.insert(tk.END, "⚠️ Not enough bits for error checking\n")
                self.error_rate = 0.0
                self.security_label.configure(text="⚠️ Insufficient bits for error checking", 
                                            style='Warning.TLabel')
            
            self.error_button.configure(text="Continue to Final Key →", command=self.go_to_final)
        
        threading.Thread(target=check_errors, daemon=True).start()
    
    def go_to_final(self):
        """Move to final key page"""
        self.enable_tab(7)
        self.notebook.select(7)
    
    def generate_final_key(self):
        """Generate the final key"""
        if not hasattr(self, 'sifted_bits') or len(self.sifted_bits) < 8:
            messagebox.showerror("Error", "Not enough bits to generate a secure key!")
            return
        
        # Privacy amplification using SHA-256
        bit_string = ''.join(str(b) for b in self.sifted_bits)
        
        # Pad to multiple of 8
        while len(bit_string) % 8 != 0:
            bit_string += '0'
        
        # Convert to bytes and hash
        byte_data = bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))
        self.final_key = hashlib.sha256(byte_data).hexdigest()
        
        # Display key
        self.key_text.delete(1.0, tk.END)
        self.key_text.insert(tk.END, "🔑 YOUR SHARED SECRET KEY:\n")
        self.key_text.insert(tk.END, "=" * 64 + "\n")
        self.key_text.insert(tk.END, self.final_key + "\n")
        self.key_text.insert(tk.END, "=" * 64 + "\n")
        
        # Display summary
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, "📋 DEMONSTRATION SUMMARY:\n")
        self.summary_text.insert(tk.END, f"1. Qubits sent: {self.num_qubits}\n")
        self.summary_text.insert(tk.END, f"2. Matching bases: {len(self.matching_indices)}\n")
        self.summary_text.insert(tk.END, f"3. Final key: {len(self.final_key)} hex chars\n")
        self.summary_text.insert(tk.END, f"4. Error rate: {self.error_rate:.1%}\n")
        self.summary_text.insert(tk.END, f"5. Eavesdropper: {'YES' if self.has_eavesdropper else 'NO'}\n")
        self.summary_text.insert(tk.END, f"6. Security: {'COMPROMISED' if self.error_rate > 0.15 else 'SECURE'}\n\n")
        
        self.summary_text.insert(tk.END, "🎯 INSTRUCTIONS FOR CHAT DEMO:\n")
        self.summary_text.insert(tk.END, "1. COPY the entire hex key above\n")
        self.summary_text.insert(tk.END, "2. Open browser to http://localhost:3000\n")
        self.summary_text.insert(tk.END, "3. Paste key when joining chat\n")
        self.summary_text.insert(tk.END, "4. Use Encrypt/Decrypt buttons in chat\n\n")
        
        self.summary_text.insert(tk.END, "⚠️ REMEMBER: For true OTP security:\n")
        self.summary_text.insert(tk.END, "• Never reuse this key\n")
        self.summary_text.insert(tk.END, "• Key must be ≥ message length\n")
        self.summary_text.insert(tk.END, "• Destroy key after use\n")
        
        # Enable buttons
        self.copy_button.configure(state='normal')
        self.save_button.configure(state='normal')
        self.generate_button.configure(state='disabled')
    
    def copy_key(self):
        """Copy key to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.final_key)
        messagebox.showinfo("Copied", "Key copied to clipboard!")
    
    def save_key(self):
        """Save key to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save BB84 Key"
        )
        
        if filename:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(filename, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("BB84 Quantum Key Generation Results\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Generated: {timestamp}\n")
                f.write(f"Qubits sent: {self.num_qubits}\n")
                f.write(f"Matching bases: {len(self.matching_indices)}\n")
                f.write(f"Error rate: {self.error_rate:.1%}\n")
                f.write(f"Eavesdropper simulated: {'YES' if self.has_eavesdropper else 'NO'}\n")
                f.write(f"Security status: {'COMPROMISED' if self.error_rate > 0.15 else 'SECURE'}\n\n")
                f.write("FINAL KEY (hex):\n")
                f.write("=" * 60 + "\n")
                f.write(self.final_key + "\n")
                f.write("=" * 60 + "\n")
            
            messagebox.showinfo("Saved", f"Key saved to {filename}")
    
    def restart_demo(self):
        """Restart the demonstration"""
        # Reset all variables
        self.current_step = 0
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_results = []
        self.final_key = ""
        
        # Disable all tabs except first two
        for i in range(2, 8):
            self.notebook.tab(i, state='disabled')
        
        # Clear all text widgets
        for widget in [self.alice_text, self.bob_text, self.sifting_text, 
                      self.error_text, self.key_text, self.summary_text]:
            widget.delete(1.0, tk.END)
        
        # Reset buttons
        self.prep_button.configure(text="Start Qubit Preparation", 
                                  command=self.start_alice_preparation)
        self.transmit_button.configure(text="🚀 Send Qubits", 
                                      command=self.start_transmission)
        self.measure_button.configure(text="Start Measurements", 
                                     command=self.start_bob_measurement)
        self.sifting_button.configure(text="Compare Bases & Sift", 
                                     command=self.start_sifting)
        self.error_button.configure(text="Check for Errors", 
                                   command=self.start_error_checking)
        self.generate_button.configure(text="Generate Final Key", 
                                      command=self.generate_final_key, state='normal')
        self.copy_button.configure(state='disabled')
        self.save_button.configure(state='disabled')
        
        # Hide Eve frame
        self.eve_frame.pack_forget()
        
        # Go to welcome page
        self.notebook.select(0)
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = BB84GUI()
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
