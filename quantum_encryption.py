# import random
# import hashlib
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# class QuantumEncryptionService:
#     @staticmethod
#     def encrypt_message(message: str, key_hex: str):
#         """Encrypt message using OTP"""
#         try:
#             # Convert hex key to bytes
#             key_bytes = bytes.fromhex(key_hex)
#             key_bits = []
#             for byte in key_bytes:
#                 key_bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
            
#             # Convert message to bits
#             message_bytes = message.encode('utf-8')
#             message_bits = []
#             for byte in message_bytes:
#                 message_bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
            
#             if len(key_bits) < len(message_bits):
#                 return {
#                     "success": False,
#                     "error": f"Key too short! Need {len(message_bits)} bits, have {len(key_bits)} bits"
#                 }
            
#             # OTP encryption (XOR)
#             cipher_bits = []
#             for m_bit, k_bit in zip(message_bits, key_bits):
#                 cipher_bits.append(m_bit ^ k_bit)
            
#             # Convert to hex
#             cipher_string = ''.join(str(b) for b in cipher_bits)
#             cipher_bytes = bytes(int(cipher_string[i:i+8], 2) 
#                                for i in range(0, len(cipher_string), 8))
            
#             return {
#                 "success": True,
#                 "encrypted_hex": cipher_bytes.hex(),
#                 "key_used": key_hex[:16] + "...",
#                 "message_length": len(message)
#             }
#         except Exception as e:
#             return {"success": False, "error": str(e)}
    
#     @staticmethod
#     def decrypt_message(encrypted_hex: str, key_hex: str):
#         """Decrypt message using OTP"""
#         try:
#             # Convert hex key to bits
#             key_bytes = bytes.fromhex(key_hex)
#             key_bits = []
#             for byte in key_bytes:
#                 key_bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
            
#             # Convert ciphertext to bits
#             cipher_bytes = bytes.fromhex(encrypted_hex)
#             cipher_bits = []
#             for byte in cipher_bytes:
#                 cipher_bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
            
#             if len(key_bits) < len(cipher_bits):
#                 return {
#                     "success": False,
#                     "error": f"Key too short! Need {len(cipher_bits)} bits, have {len(key_bits)} bits"
#                 }
            
#             # OTP decryption (XOR)
#             plain_bits = []
#             for c_bit, k_bit in zip(cipher_bits, key_bits):
#                 plain_bits.append(c_bit ^ k_bit)
            
#             # Convert to string
#             plain_string = ''.join(str(b) for b in plain_bits)
#             plain_bytes = bytes(int(plain_string[i:i+8], 2) 
#                               for i in range(0, len(plain_string), 8))
            
#             decrypted_message = plain_bytes.decode('utf-8')
#             return {
#                 "success": True,
#                 "decrypted_message": decrypted_message,
#                 "key_used": key_hex[:16] + "..."
#             }
#         except Exception as e:
#             return {"success": False, "error": str(e)}

# @app.route('/api/encrypt', methods=['POST'])
# def encrypt():
#     data = request.json
#     message = data.get('message', '')
#     key = data.get('key', '')
    
#     if not message or not key:
#         return jsonify({"success": False, "error": "Message and key required"})
    
#     result = QuantumEncryptionService.encrypt_message(message, key)
#     return jsonify(result)

# @app.route('/api/decrypt', methods=['POST'])
# def decrypt():
#     data = request.json
#     encrypted = data.get('encrypted', '')
#     key = data.get('key', '')
    
#     if not encrypted or not key:
#         return jsonify({"success": False, "error": "Encrypted text and key required"})
    
#     result = QuantumEncryptionService.decrypt_message(encrypted, key)
#     return jsonify(result)

# @app.route('/api/health', methods=['GET'])
# def health():
#     return jsonify({"status": "healthy", "service": "Quantum Encryption"})

# if __name__ == '__main__':
#     print("🔐 Quantum Encryption Service")
#     print("Running on http://localhost:5001")
#     print("Endpoints:")
#     print("  POST /api/encrypt - Encrypt message with OTP")
#     print("  POST /api/decrypt - Decrypt message with OTP")
#     print("  GET  /api/health  - Health check")
#     app.run(host='0.0.0.0', port=5001, debug=True)

import random
import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    message = data.get('message', '')
    key = data.get('key', '')
    
    if not message or not key:
        return jsonify({"success": False, "error": "Message and key required"})
    
    try:
        # Simple OTP encryption
        key_bytes = bytes.fromhex(key)
        key_bits = []
        for byte in key_bytes:
            key_bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
        
        message_bytes = message.encode('utf-8')
        message_bits = []
        for byte in message_bytes:
            message_bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
        
        if len(key_bits) < len(message_bits):
            return jsonify({
                "success": False,
                "error": f"Key too short! Need {len(message_bits)} bits, have {len(key_bits)} bits"
            })
        
        # XOR encryption
        cipher_bits = []
        for m_bit, k_bit in zip(message_bits, key_bits):
            cipher_bits.append(m_bit ^ k_bit)
        
        cipher_string = ''.join(str(b) for b in cipher_bits)
        cipher_bytes = bytes(int(cipher_string[i:i+8], 2) 
                           for i in range(0, len(cipher_string), 8))
        
        return jsonify({
            "success": True,
            "encrypted_hex": cipher_bytes.hex(),
            "message_length": len(message),
            "bits_encrypted": len(message_bits)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    encrypted = data.get('encrypted', '')
    key = data.get('key', '')
    
    if not encrypted or not key:
        return jsonify({"success": False, "error": "Encrypted text and key required"})
    
    try:
        # Simple OTP decryption (same as encryption)
        key_bytes = bytes.fromhex(key)
        key_bits = []
        for byte in key_bytes:
            key_bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
        
        cipher_bytes = bytes.fromhex(encrypted)
        cipher_bits = []
        for byte in cipher_bytes:
            cipher_bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
        
        if len(key_bits) < len(cipher_bits):
            return jsonify({
                "success": False,
                "error": f"Key too short! Need {len(cipher_bits)} bits, have {len(key_bits)} bits"
            })
        
        # XOR decryption
        plain_bits = []
        for c_bit, k_bit in zip(cipher_bits, key_bits):
            plain_bits.append(c_bit ^ k_bit)
        
        plain_string = ''.join(str(b) for b in plain_bits)
        plain_bytes = bytes(int(plain_string[i:i+8], 2) 
                          for i in range(0, len(plain_string), 8))
        
        decrypted_message = plain_bytes.decode('utf-8')
        
        return jsonify({
            "success": True,
            "decrypted_message": decrypted_message
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "Quantum Encryption"})

if __name__ == '__main__':
    print("🔐 Quantum Encryption Service")
    print("Running on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)