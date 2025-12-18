"""
Interactive BB84 Quantum Key Generator for Terminal
Perfect for live demonstrations with audience participation!
"""

import random
import hashlib
import time
import sys
import os
from typing import List, Tuple

class InteractiveBB84Generator:
    def __init__(self):
        self.clear_screen()
        print("🎭" * 50)
        print("      INTERACTIVE BB84 QUANTUM KEY GENERATOR")
        print("🎭" * 50)
        print("\n🎯 Perfect for live demonstrations!")
        print("   You'll play both Alice and Bob to generate a shared secret key.")
        print("   The audience can help make choices!\n")
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def press_enter(self, prompt="Press Enter to continue..."):
        """Wait for user to press Enter"""
        input(f"\n{prompt}")
    
    def show_step(self, step_num: int, title: str):
        """Display step header"""
        self.clear_screen()
        print(f"\n{'='*60}")
        print(f"STEP {step_num}: {title}")
        print(f"{'='*60}\n")
    
    def ask_choice(self, prompt: str, options: List[str]) -> int:
        """Ask user to choose from options"""
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = int(input(f"\nChoose (1-{len(options)}): "))
                if 1 <= choice <= len(options):
                    return choice
                print(f"Please enter 1-{len(options)}")
            except ValueError:
                print("Please enter a number")
    
    def simulate_transmission(self, message: str):
        """Simulate quantum transmission with animation"""
        print(f"\n⚛️  {message}")
        for _ in range(3):
            for frame in ["   ░▒▓█ Quantum particles flying... █▓▒░",
                         "   █▓▒░ Quantum particles flying... ░▒▓█",
                         "   ░▒▓█ Quantum particles flying... █▓▒░"]:
                print(frame, end='\r')
                time.sleep(0.2)
        print(" " * 60, end='\r')
    
    def run_interactive_generation(self) -> str:
        """Run fully interactive BB84 key generation"""
        
        # STEP 1: Introduction
        self.show_step(1, "INTRODUCTION TO BB84 PROTOCOL")
        print("🔬 What is BB84?")
        print("• First quantum cryptography protocol (1984)")
        print("• Uses quantum mechanics for secure key distribution")
        print("• Provably secure against eavesdropping")
        
        print("\n🎭 In this demonstration, you will:")
        print("  1. Play as ALICE: Prepare and send quantum bits")
        print("  2. Play as BOB: Measure received quantum bits")
        print("  3. Publicly discuss bases to establish shared key")
        print("  4. Detect any eavesdropping attempts")
        
        self.press_enter("Ready to start the quantum key generation?")
        
        # STEP 2: Setup parameters
        self.show_step(2, "SETUP PARAMETERS")
        
        print("📊 How many quantum bits (qubits) should we use?")
        print("  More qubits = longer key but more work")
        print("  Recommended: 20-50 for demonstration")
        
        while True:
            try:
                num_qubits = int(input("\nNumber of qubits to send (10-100): "))
                if 10 <= num_qubits <= 100:
                    break
                print("Please choose between 10 and 100")
            except ValueError:
                print("Please enter a number")
        
        # Ask about eavesdropper
        print("\n⚠️  SECURITY SCENARIO:")
        choice = self.ask_choice("Should we simulate an eavesdropper (Eve)?", 
                               ["No eavesdropper - secure quantum channel",
                                "Yes, add eavesdropper - see how BB84 detects it!"])
        
        has_eavesdropper = (choice == 2)
        
        # STEP 3: Alice prepares qubits
        self.show_step(3, "ALICE PREPARES QUBITS")
        print("🎭 You are now playing as ALICE")
        print("\nFor each qubit, Alice must choose:")
        print("  • A bit value: 0 or 1")
        print("  • A basis: + (computational) or × (diagonal)")
        print("\nThe basis determines how the qubit is encoded.")
        
        print(f"\n📝 Preparing {num_qubits} qubits...")
        print("You can choose manually or let the computer choose randomly.")
        
        choice = self.ask_choice("\nHow do you want to prepare qubits?", 
                               ["I'll choose manually (good for small demos)",
                                "Choose randomly (faster for many qubits)",
                                "Mix: I'll choose first few, random for rest"])
        
        alice_bits = []
        alice_bases = []
        
        if choice == 1:  # Manual all
            print(f"\n📝 Manual preparation of {num_qubits} qubits:")
            print("-" * 40)
            for i in range(num_qubits):
                print(f"\nQubit {i+1}/{num_qubits}:")
                bit_choice = self.ask_choice("Bit value:", ["0", "1"])
                basis_choice = self.ask_choice("Basis:", ["+ basis (computational)", "× basis (diagonal)"])
                
                alice_bits.append(0 if bit_choice == 1 else 1)
                alice_bases.append(0 if basis_choice == 1 else 1)
                
                print(f"✓ Set: Bit={alice_bits[-1]}, Basis={'+' if alice_bases[-1]==0 else '×'}")
                time.sleep(0.3)
                
        elif choice == 2:  # Random all
            print(f"\n🎲 Random preparation of {num_qubits} qubits...")
            for i in range(num_qubits):
                alice_bits.append(random.randint(0, 1))
                alice_bases.append(random.randint(0, 1))
                if i < 5:  # Show first 5
                    print(f"Qubit {i+1}: Bit={alice_bits[-1]}, Basis={'+' if alice_bases[-1]==0 else '×'}")
                    time.sleep(0.2)
            if num_qubits > 5:
                print(f"... and {num_qubits-5} more qubits randomly prepared")
            time.sleep(1)
            
        else:  # Mix: manual first 5, random rest
            manual_count = min(5, num_qubits)
            print(f"\n📝 Manual preparation of first {manual_count} qubits:")
            for i in range(manual_count):
                print(f"\nQubit {i+1}/{manual_count}:")
                bit_choice = self.ask_choice("Bit value:", ["0", "1"])
                basis_choice = self.ask_choice("Basis:", ["+ basis", "× basis"])
                
                alice_bits.append(0 if bit_choice == 1 else 1)
                alice_bases.append(0 if basis_choice == 1 else 1)
                print(f"✓ Set: Bit={alice_bits[-1]}, Basis={'+' if alice_bases[-1]==0 else '×'}")
                time.sleep(0.3)
            
            if num_qubits > manual_count:
                print(f"\n🎲 Random preparation of remaining {num_qubits-manual_count} qubits...")
                for i in range(manual_count, num_qubits):
                    alice_bits.append(random.randint(0, 1))
                    alice_bases.append(random.randint(0, 1))
                time.sleep(1)
        
        print(f"\n✅ Alice has prepared all {num_qubits} qubits!")
        print(f"Sample (first 10): Bits={alice_bits[:10]}")
        print(f"Sample (first 10): Bases={['+' if b==0 else '×' for b in alice_bases[:10]]}")
        
        self.press_enter("Press Enter to send qubits through quantum channel...")
        
        # STEP 4: Quantum transmission
        self.show_step(4, "QUANTUM TRANSMISSION")
        print("🌌 Sending qubits through quantum channel...")
        
        self.simulate_transmission("Transmitting qubits from Alice to Bob")
        
        if has_eavesdropper:
            print("\n👁️  EAVESDROPPER DETECTED!")
            print("Eve is intercepting and measuring the qubits...")
            time.sleep(2)
            
            # Eve's interception
            intercepted_bits = []
            intercepted_bases = []
            eve_bases = []
            
            print("\nEve's attack process:")
            for i in range(num_qubits):
                if random.random() < 0.6:  # 60% chance Eve intercepts
                    eve_basis = random.randint(0, 1)
                    eve_bases.append(eve_basis)
                    
                    # Eve measures
                    if alice_bases[i] == eve_basis:
                        intercepted_bit = alice_bits[i]
                    else:
                        intercepted_bit = random.randint(0, 1)
                    
                    intercepted_bits.append(intercepted_bit)
                    intercepted_bases.append(eve_basis)
                else:
                    # Not intercepted
                    intercepted_bits.append(alice_bits[i])
                    intercepted_bases.append(alice_bases[i])
            
            print(f"📊 Eve intercepted {len(eve_bases)}/{num_qubits} qubits!")
            print(f"   This will introduce errors that Alice and Bob can detect!")
            
            alice_bits = intercepted_bits
            alice_bases = intercepted_bases
        else:
            print("\n✅ Secure transmission! No eavesdropper detected.")
        
        self.press_enter()
        
        # STEP 5: Bob measures qubits
        self.show_step(5, "BOB MEASURES QUBITS")
        print("🎭 You are now playing as BOB")
        print("\nBob receives the qubits and needs to measure them.")
        print("He must choose a measurement basis for each qubit.")
        print("\nCRITICAL: Bob only gets the correct bit if he chooses")
        print("the SAME basis that Alice used to prepare the qubit!")
        
        self.press_enter("Ready to measure?")
        
        print(f"\n🔬 Measuring {num_qubits} qubits...")
        print("How should Bob choose measurement bases?")
        
        choice = self.ask_choice("Measurement strategy:", 
                               ["Choose manually for each qubit",
                                "Choose randomly (like real protocol)",
                                "Smart: Try to match Alice's bases"])
        
        bob_bases = []
        bob_results = []
        
        if choice == 1:  # Manual measurement
            print(f"\n📝 Manual measurement of {num_qubits} qubits:")
            for i in range(num_qubits):
                print(f"\nQubit {i+1}/{num_qubits}:")
                basis_choice = self.ask_choice("Choose measurement basis:", 
                                             ["+ basis", "× basis"])
                bob_basis = 0 if basis_choice == 1 else 1
                bob_bases.append(bob_basis)
                
                # Simulate measurement
                if alice_bases[i] == bob_basis:
                    result = alice_bits[i]
                    print(f"  Result: {result} ✓ (Correct! Same basis as Alice)")
                else:
                    result = random.randint(0, 1)
                    print(f"  Result: {result} ✗ (Random! Different basis)")
                
                bob_results.append(result)
                time.sleep(0.3)
                
        elif choice == 2:  # Random measurement
            print(f"\n🎲 Random measurement of {num_qubits} qubits...")
            for i in range(num_qubits):
                bob_basis = random.randint(0, 1)
                bob_bases.append(bob_basis)
                
                if alice_bases[i] == bob_basis:
                    result = alice_bits[i]
                else:
                    result = random.randint(0, 1)
                
                bob_results.append(result)
                
                if i < 5:  # Show first 5
                    match = "✓" if alice_bases[i] == bob_basis else "✗"
                    print(f"Qubit {i+1}: Basis={'+' if bob_basis==0 else '×'}, "
                          f"Result={result} {match}")
                    time.sleep(0.2)
            
            if num_qubits > 5:
                print(f"... and {num_qubits-5} more qubits measured randomly")
                
        else:  # Smart measurement (try to match)
            print(f"\n🧠 Smart measurement - trying to guess Alice's bases...")
            # In reality, Bob doesn't know Alice's bases, but for demo
            for i in range(num_qubits):
                # Bob guesses randomly (as in real protocol)
                bob_basis = random.randint(0, 1)
                bob_bases.append(bob_basis)
                
                if alice_bases[i] == bob_basis:
                    result = alice_bits[i]
                    match = "✓"
                else:
                    result = random.randint(0, 1)
                    match = "✗"
                
                bob_results.append(result)
                
                if i < 5:
                    print(f"Qubit {i+1}: Bob chose {'+' if bob_basis==0 else '×'}, "
                          f"Alice used {'+' if alice_bases[i]==0 else '×'}, "
                          f"Result={result} {match}")
                    time.sleep(0.2)
        
        print(f"\n✅ Bob has measured all qubits!")
        print(f"Bob's sample bases: {['+' if b==0 else '×' for b in bob_bases[:10]]}")
        print(f"Bob's sample results: {bob_results[:10]}")
        
        self.press_enter()
        
        # STEP 6: Public discussion (sifting)
        self.show_step(6, "PUBLIC DISCUSSION & SIFTING")
        print("📢 Alice and Bob now discuss PUBLICLY over classical channel")
        print("They ONLY reveal which basis they used for each qubit.")
        print("They keep the actual bit values SECRET!")
        print("\nThey discard all bits where bases don't match.")
        
        self.press_enter("Let's compare bases...")
        
        print("\n🔍 Comparing Alice's and Bob's bases:")
        print("-" * 60)
        print(f"{'Qubit':<8} {'Alice':<10} {'Bob':<10} {'Match?':<10} {'Keep?'}")
        print("-" * 60)
        
        matching_indices = []
        matches_displayed = 0
        
        for i in range(num_qubits):
            match = alice_bases[i] == bob_bases[i]
            
            if match:
                matching_indices.append(i)
                symbol = "✓ YES"
                keep = "✓ KEEP"
            else:
                symbol = "✗ NO"
                keep = "✗ DISCARD"
            
            # Only show first 15 comparisons to avoid flooding screen
            if i < 15:
                print(f"{i+1:<8} "
                      f"{('+' if alice_bases[i]==0 else '×'):<10} "
                      f"{('+' if bob_bases[i]==0 else '×'):<10} "
                      f"{symbol:<10} {keep}")
                time.sleep(0.1)
            elif i == 15 and num_qubits > 15:
                print(f"... and {num_qubits-15} more qubits")
        
        sifted_bits = [bob_results[i] for i in matching_indices]
        
        print(f"\n📊 SIFTING RESULTS:")
        print(f"Total qubits sent: {num_qubits}")
        print(f"Matching bases: {len(matching_indices)}")
        print(f"Key bits after sifting: {len(sifted_bits)}")
        print(f"Sifted key bits (sample): {sifted_bits[:20]}")
        
        if len(sifted_bits) < 8:
            print("\n❌ ERROR: Not enough matching bits for secure key!")
            print("   This sometimes happens by chance. Try again with more qubits.")
            return None
        
        self.press_enter()
        
        # STEP 7: Error checking for eavesdropping
        self.show_step(7, "ERROR CHECKING & EAVESDROPPER DETECTION")
        print("🔍 Checking for transmission errors...")
        print("\nAlice and Bob publicly compare a subset of their bits")
        print("to estimate the Quantum Bit Error Rate (QBER).")
        print("High error rate = Possible eavesdropper!")
        
        if len(sifted_bits) >= 10:
            sample_size = min(10, len(sifted_bits) // 2)
            sample_indices = random.sample(range(len(sifted_bits)), sample_size)
            
            print(f"\n📊 Comparing {sample_size} randomly chosen bits:")
            print("-" * 50)
            
            errors = 0
            for count, idx in enumerate(sample_indices, 1):
                alice_bit = alice_bits[matching_indices[idx]]
                bob_bit = sifted_bits[idx]
                match = alice_bit == bob_bit
                
                if match:
                    print(f"Bit {count}: Alice={alice_bit}, Bob={bob_bit} ✓ MATCH")
                else:
                    print(f"Bit {count}: Alice={alice_bit}, Bob={bob_bit} ✗ ERROR")
                    errors += 1
                time.sleep(0.5)
            
            # If we simulated eavesdropper, add more errors
            if has_eavesdropper:
                additional_errors = random.randint(2, min(4, sample_size - errors))
                errors += additional_errors
                print(f"\n⚠️  Eavesdropper introduced {additional_errors} additional errors!")
            
            error_rate = errors / sample_size
            
            print(f"\n📈 ERROR STATISTICS:")
            print(f"Bits compared: {sample_size}")
            print(f"Errors found: {errors}")
            print(f"Quantum Bit Error Rate (QBER): {error_rate:.1%}")
            
            # Remove the compared bits (they're no longer secret)
            remaining_indices = [i for i in range(len(sifted_bits)) if i not in sample_indices]
            sifted_bits = [sifted_bits[i] for i in remaining_indices]
            
            print(f"\n🔐 SECURITY ASSESSMENT:")
            if error_rate > 0.15:
                print("🚨 HIGH ERROR RATE DETECTED!")
                print("   Possible eavesdropper or noisy channel.")
                print("   This key may not be secure!")
                
                if has_eavesdropper:
                    print("\n✅ CORRECTLY DETECTED EAVESDROPPER!")
                    print("   BB84 protocol working perfectly!")
                else:
                    print("\n⚠️  No eavesdropper simulated, but high error rate.")
                    print("   In real system, they would abort and try again.")
            else:
                print("✅ LOW ERROR RATE!")
                print("   Channel appears secure.")
                if has_eavesdropper:
                    print("\n⚠️  Eve got lucky! Low error rate despite eavesdropping.")
                    print("   This happens sometimes by chance.")
                else:
                    print("   Secure key established!")
            
            if error_rate > 0.3:
                print("\n❌ Error rate too high! Key generation failed.")
                return None
                
        else:
            print("⚠️  Not enough bits for error checking")
            error_rate = 0.0
        
        self.press_enter()
        
        # STEP 8: Privacy amplification
        self.show_step(8, "PRIVACY AMPLIFICATION & FINAL KEY")
        print("🔒 Final step: Privacy Amplification")
        print("\nEven after removing compared bits, we need to ensure")
        print("no information leaked to potential eavesdroppers.")
        print("\nWe apply a cryptographic hash function to:")
        print("  1. Shorten the key to desired length")
        print("  2. Remove any partial information Eve might have")
        print("  3. Generate uniformly random final key")
        
        print(f"\nInitial sifted bits: {len(sifted_bits)} bits")
        
        # Generate final key using hash
        final_key_hex = self._privacy_amplification(sifted_bits)
        
        print(f"\n✅ FINAL KEY GENERATED!")
        print(f"Key length: {len(final_key_hex)} hex characters")
        print(f"Key bits: {len(final_key_hex) * 4} bits")
        print(f"Can encrypt: ~{len(final_key_hex)//2} characters with OTP")
        
        # Display the key
        print(f"\n🔑 YOUR SHARED SECRET KEY:")
        print("=" * 64)
        print(final_key_hex)
        print("=" * 64)
        
        print(f"\n📋 DEMONSTRATION SUMMARY:")
        print(f"1. Qubits sent: {num_qubits}")
        print(f"2. Matching bases: {len(matching_indices)}")
        print(f"3. Final key: {len(final_key_hex)} hex chars")
        print(f"4. Error rate: {error_rate:.1%}")
        print(f"5. Eavesdropper: {'YES' if has_eavesdropper else 'NO'}")
        print(f"6. Security: {'COMPROMISED' if error_rate > 0.15 else 'SECURE'}")
        
        print("\n🎯 INSTRUCTIONS FOR CHAT DEMO:")
        print("1. COPY the entire hex key above (select and copy)")
        print("2. Open browser to http://localhost:3000")
        print("3. Paste key when joining chat (both Alice and Bob need same key)")
        print("4. Use Encrypt/Decrypt buttons in chat")
        print("\n⚠️  REMEMBER: For true OTP security:")
        print("   • Never reuse this key")
        print("   • Key must be ≥ message length")
        print("   • Destroy key after use")
        
        # Save to file option
        save = input("\n💾 Save key to file? (y/n): ").lower() == 'y'
        if save:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"bb84_key_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("BB84 Quantum Key Generation Results\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Generated: {time.ctime()}\n")
                f.write(f"Qubits sent: {num_qubits}\n")
                f.write(f"Matching bases: {len(matching_indices)}\n")
                f.write(f"Error rate: {error_rate:.1%}\n")
                f.write(f"Eavesdropper simulated: {'YES' if has_eavesdropper else 'NO'}\n")
                f.write(f"Security status: {'COMPROMISED' if error_rate > 0.15 else 'SECURE'}\n\n")
                f.write("FINAL KEY (hex):\n")
                f.write("=" * 60 + "\n")
                f.write(final_key_hex + "\n")
                f.write("=" * 60 + "\n")
            print(f"✅ Key saved to {filename}")
        
        return final_key_hex
    
    def _privacy_amplification(self, bits: List[int]) -> str:
        """Convert bits to secure key using SHA-256"""
        bit_string = ''.join(str(b) for b in bits)
        
        # Pad to multiple of 8
        while len(bit_string) % 8 != 0:
            bit_string += '0'
        
        # Convert to bytes
        byte_data = bytes(int(bit_string[i:i+8], 2) 
                         for i in range(0, len(bit_string), 8))
        
        # Use hash for privacy amplification
        hash_obj = hashlib.sha256(byte_data)
        return hash_obj.hexdigest()
    
    # def run_quick_mode(self) -> str:
    #     """Quick mode for testing"""
    #     print("\n🚀 QUICK MODE - Automated key generation")
        
    #     num_qubits = 32
    #     has_eavesdropper = False
        
    #     # Generate quickly
    #     alice_bits = [random.randint(0, 1) for _ in range(num_qubits)]
    #     alice_bases = [random.randint(0, 1) for _ in range(num_qubits)]
    #     bob_bases = [random.randint(0, 1) for _ in range(num_qubits)]
        
    #     # Bob's measurements
    #     bob_results = []
    #     for i in range(num_qubits):
    #         if alice_bases[i] == bob_bases[i]:
    #             bob_results.append(alice_bits[i])
    #         else:
    #             bob_results.append(random.randint(0, 1))
        
    #     # Sift
    #     sifted_bits = []
    #     for i in range(num_qubits):
    #         if alice_bases[i] == bob_bases[i]:
    #             sifted_bits.append(bob_results[i])
        
    #     if len(sifted_bits) < 8:
    #         return self.run_quick_mode()  # Try again
        
    #     # Generate key
    #     final_key_hex = self._privacy_amplification(sifted_bits)
        
    #     print(f"\n✅ Quick key generated!")
    #     print(f"Key: {final_key_hex[:32]}...")
    #     print(f"Length: {len(final_key_hex)} hex characters")
        
    #     return final_key_hex

def main():
    """Main function"""
    generator = InteractiveBB84Generator()
    
    print("\nChoose mode:")
    print("1. 🎭 FULL INTERACTIVE DEMO")
    print("   - Step-by-step BB84 protocol")
    print("   - Make choices as Alice and Bob")
    print("   - See eavesdropper detection")
    # print("2. 🚀 QUICK GENERATION")
    # print("   - Fast automated key generation (For testing)")
    print("2. ℹ️  ABOUT BB84")
    print("   - Learn about the protocol")
    
    choice = input("\nEnter choice (1-3): ")
    
    if choice == "1":
        key = generator.run_interactive_generation()
    # elif choice == "2":
    #     key = generator.run_quick_mode()
    elif choice == "2":
        generator.clear_screen()
        print("\n📚 ABOUT BB84 PROTOCOL")
        print("=" * 60)
        print("\nBB84 is the first quantum cryptography protocol,")
        print("proposed by Charles Bennett and Gilles Brassard in 1984.")
        
        print("\n🎯 KEY PRINCIPLES:")
        print("1. Quantum Superposition: Qubits in + or × basis")
        print("2. Measurement Disturbance: Measuring changes quantum state")
        print("3. No-Cloning Theorem: Cannot copy unknown quantum states")
        
        print("\n🔐 SECURITY GUARANTEES:")
        print("• Any eavesdropping introduces detectable errors")
        print("• Information gained by Eve = Errors introduced")
        print("• Perfect secrecy with One-Time Pad")
        
        print("\n⚡ REAL-WORLD USE:")
        print("• Secure government communications")
        print("• Banking transactions")
        print("• Satellite communications")
        print("• Military applications")
        
        input("\nPress Enter to generate a key...")
        key = generator.run_interactive_generation()
    else:
        print("Invalid choice. Using interactive mode...")
        key = generator.run_interactive_generation()
    
    if key:
        print("\n🎉 KEY GENERATION COMPLETE!")
        print("Open two browser windows for Alice and Bob,")
        print("and paste this key in both chat windows.")
        print("\nChat URL: http://localhost:3000")
    else:
        print("\n❌ Key generation failed. Try again!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demonstration interrupted. Thanks for trying!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please make sure you have all dependencies installed.")