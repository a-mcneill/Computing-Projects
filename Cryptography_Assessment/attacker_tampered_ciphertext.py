"""
The purpose of this code file is to act as an attacker who is able to pass the forged identity and authentication tested in attacker_forged_identity and to test for
ciphertext tampering.

This testing will effectively use the angus.py with changes to the nonce and ciphertext - i.e., a fake nonce and ciphertext, in order to demonstrate robustness against
MITM ciphertext tampering attacks.
"""


# Student ID: 36305138
# Student Name: Alexander McNeill


# Imports -> same as bobby file:
    # import socket module in order to establish a connection for demonstration over the network
import socket
    # import functions from the identity_authentication code file for the generation and verification of RSA key and verification of signature
from identity_authentication import generate_rsa_identity_key, generate_public_identity_bytes, convert_public_identity_key, sign_authentication_data, verify_rsa_signature
    # import functions from the dh_engine code file for the generation of Diffie-Hellman key pair and the computation of the shared secret
from dh_engine import generate_private_key, get_public_key_bytes, convert_bytes_to_key, calculate_shared_key
    # import functions from the crypto_confidentiality_integrity code file for the generation of the SHA256 AES-GCM key and encryption of the plaintext to AES-GCM ciphertext
from crypto_confidentiality_integrity import convert_sharedsecret_symmetric_key, encrypt_plaintext_ciphertext



# implementation of send and receive message functions - ensure keys are fully sent and received

def send_msg(socket, data: bytes):
    """The purpose of this function is to send a 4-byte big-endian length prefix followed by the raw data, ensuring the receiver knows exactly how many bytes to read."""

    length = len(data).to_bytes(4, 'big')   # using big-endian 4 byte length
    socket.sendall(length)
    socket.sendall(data)


def recv_msg(socket) -> bytes:
    """The purpose of this function is to receive a length-prefixed message to ensure all data in bytes format is received. 
        Raises a ConnectionError if the connection closes before all bytes are received.
        The function reads the 4-byte big-endian length, then reads exactly that many bytes."""

    length_bytes = socket.recv(4)

    if not length_bytes:
        raise ConnectionError("Connection closed while reading length.")
    
    length = int.from_bytes(length_bytes, 'big')

    data = b''

    while len(data) < length:
        chunk = socket.recv(length - len(data))

        if not chunk:
            raise ConnectionError("Connection closed while reading data.")
        
        data += chunk

    return data



# --------------------------------------------------------------------

# Step 1: Generation of attacker's RSA identity keys for identity authentication -> private key and public key in bytes form
attacker_rsa_private = generate_rsa_identity_key()

attacker_rsa_public_bytes = generate_public_identity_bytes(attacker_rsa_private)


# --------------------------------------------------------------------

# Step 2: Generate attacker's Diffie-Hellman key pair -> again, private key and public key in byte format
attacker_DH_private = generate_private_key()

attacker_DH_public_bytes = get_public_key_bytes(attacker_DH_private)


# --------------------------------------------------------------------

# Step 3: Connect to Bobby's socket session
    # As highlighted in bobby file, Angus is the sender so will connect to the socket connection opened by Bobby

attacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # using AF_INET == Address family is IPv4 addresses
    # SOCK_STREAM is using a TCP socket stream based communication

attacker_socket.connect(("localhost", 8888))
    # socket connection to the local host interface on port 8888 -> 127.0.0.1:8888 Bobby is waiting here

print("[+] Welcome Attacker! You are connected to the network. Bobby is connected.")

print("[+] Beginning key exchange...")


# --------------------------------------------------------------------

# Step 4:  generate signature and sending information to other user's -> Diffie-Hellman public key (bytes), RSA public key (bytes), and user's signature for verification
    # sending keys in byte format, as well as signature, using send_msg function


attacker_signature = sign_authentication_data(attacker_rsa_private, attacker_DH_public_bytes)
    # generation of signature for verification -> using RSA private key and Diffie-Hellman public key 

send_msg(attacker_socket, attacker_DH_public_bytes)

send_msg(attacker_socket, attacker_rsa_public_bytes)

send_msg(attacker_socket, attacker_signature)

print("[+] Confirmation: Your public keys and signature have been shared.")


# --------------------------------------------------------------------

# Step 5: Recieve other user's Diffie-Hellman key, RSA key, and signature
     # receiving keys in byte format, as well as signature, with recv_msg function to ensure full bytes are received

bobby_DH_public_bytes = recv_msg(attacker_socket)

bobby_rsa_public_bytes = recv_msg(attacker_socket)

bobby_signature = recv_msg(attacker_socket)


# --------------------------------------------------------------------

# Step 6: Conversion of other user's RSA public key from bytes to the key and verification of signature
    # verifying Bobby's sgnature by calling verify_rsa_signature function with Bobby's rsa public key, signature, and Diffie-Hellman public key in bytes to confirm identity

# wrapping conversion of public key bytes in an exception for demonstration of robustness - if invalid rsa key bytes presented, exception raised and connection terminated
try:
    bobby_rsa_public_key = convert_public_identity_key(bobby_rsa_public_bytes)
except Exception as e2:
    print("[!] Error: Invalid RSA public key received. Connection terminated.")
    print(f"[!!] Details: {e2}")

    # upon verification failure, close connection
    attacker_socket.close()
    exit()


# wrapping of verificatioon of RSA signature in an explicit exception, raising exception, closing socket session, and exiting program upon verification failure
try:
    verify_rsa_signature(bobby_rsa_public_key, bobby_signature, bobby_DH_public_bytes)
except Exception as e3:
    print("[!] Error: Invalid signature. Connection terminated.")
    print(f"[!!] Details: {e3}")

    # upon verification failure
    attacker_socket.close()
    exit()

print("[+] Bobby's identity and Diffie-Hellman key has been authenticated.")
    # if not authenticated, the program will run an exception, as programmed through identity_authentication and use of cryptography library


# --------------------------------------------------------------------

# Step 7: Calculate the shared secret
    # Angus to compute the shared secret from Bobby's Diffie-Hellman public key, post byte conversion back to key, and Bobby's private Diffie-Hellman key

# wrapping Diffie-Hellman public key conversion in explicit exception, to protect against malformed key
try:
    bobby_DH_public_key = convert_bytes_to_key(bobby_DH_public_bytes)
except Exception as e4:
    print("[!] Error: Invalid Diffie-Hellman public key received. Connection terminated.")
    print(f"[!!] Details: {e4}")

    # upon verification failure, close connection
    attacker_socket.close()
    exit()

shared_secret_key = calculate_shared_key(attacker_DH_private, bobby_DH_public_key)

print("[+] Confirmation: The shared secret has been calculated.")


# --------------------------------------------------------------------

# Step 8: Generate the AES encrypted shared secret key
    # Taking the shared secret generated in step 7 and hash it in SHA256 to generate the key

aes_shared_key = convert_sharedsecret_symmetric_key(shared_secret_key)

print("[+] Confirmation: The shared key has been generated.")


# --------------------------------------------------------------------

# Step 9: Message Encryption
    # utilising AES-GCM to encrypt plaintext message into ciphertext using a randomly generated 12 byte nonce and generate AES generated shared key
    # using encode function to turn string into a byte object for transmission, to then be converted back into word string upon decryption

plaintext = "Oi Oi savoy! Can't believe West Ham got relegated. What an utter disaster, Bobby.".encode()

nonce, ciphertext = encrypt_plaintext_ciphertext(aes_shared_key, plaintext)

print("[+] Confirmation: Message created and encrypted.")


# --------------------------------------------------------------------

# Step 10: Tamper with ciphertext - Attacker
    # as this is the modified Angus for the attacker, testing the tampering of the ciphertext by flipping one bit
    # Flipping one bit ensures the AES-GCM authentication tag will fail on Bobby's side.

ciphertext = bytearray(ciphertext)

ciphertext[0] ^= 0xFF   # flipping first bit

ciphertext = bytes(ciphertext)


# --------------------------------------------------------------------


# Step 11: Sending of the nonce and ciphertext to the recipient -> Bobby then closing connection
    # again, utilising the connection on the socket joined earlier on the local host interface and open port (8888)
    # again, using send_msg function to ensure all bytes are sent and read

send_msg(attacker_socket, nonce)

send_msg(attacker_socket, ciphertext)

print("[!] Attacker: Tampered ciphertext sent.")

# explicitly closing session socket once the communication has been sent
print("[+] Session complete. Terminating communication.")
attacker_socket.close()


# --------------------------------------------------------------------