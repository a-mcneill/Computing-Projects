"""
The purpose of this code file is to act as the user who is sending the encrypted plaintext message, ciphertext, to the other user. Similarly to the recipient (Bobby) code file, 
this file will enable the generation of RSA identity keys for authentication, the Diffie-Helmman keys and shared secret, the connection to the socket on which the recipient is
waiting, the reciept of the other user's key and for the verification of their signature, and finally, the encryption and sending of the nonce and ciphertext.

Key Tasks:
    1. RSA key generation -> for identity authentication.
    2. Diffie-Hellman key pair generation -> produces the shared secret and facilitates the key exchange.
    3. Connection to the socket -> to communicate with the recipient.
    4. Sending and receiving of public keys (Diffie-Hellman and RSA) and signature
    5. Verification of other user's signature
    6. Computation of shared secret and derivation of AES encryption key
    7. Encryption of a plaintext message.
    8. Sending of nonce and ciphertext.

Again, in structuring this project, the cryptography will be imported from the three engine files (dh_engine, identity_authentication, and crypto_confidentiality_integrity), and
as such will import their functions.
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

# Step 1: Generation of Angus' RSA identity keys for identity authentication -> private key and public key in bytes form
angus_rsa_private = generate_rsa_identity_key()

angus_rsa_public_bytes = generate_public_identity_bytes(angus_rsa_private)


# --------------------------------------------------------------------

# Step 2: Generate Angus' Diffie-Hellman key pair -> again, private key and public key in byte format
angus_DH_private = generate_private_key()

angus_DH_public_bytes = get_public_key_bytes(angus_DH_private)


# --------------------------------------------------------------------

# Step 3: Connect to Bobby's socket session
    # As highlighted in bobby file, Angus is the sender so will connect to the socket connection opened by Bobby

angus_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # using AF_INET == Address family is IPv4 addresses
    # SOCK_STREAM is using a TCP socket stream based communication

angus_socket.connect(("localhost", 8888))
    # socket connection to the local host interface on port 8888 -> 127.0.0.1:8888 Bobby is waiting here

print("[+] Welcome Angus! You are connected to the network. Bobby is connected.")

print("[+] Beginning key exchange...")


# --------------------------------------------------------------------

# Step 4:  generate signature and sending information to other user's -> Diffie-Hellman public key (bytes), RSA public key (bytes), and user's signature for verification
    # sending keys in byte format, as well as signature, using send_msg function


angus_signature = sign_authentication_data(angus_rsa_private, angus_DH_public_bytes)
    # generation of signature for verification -> using RSA private key and Diffie-Hellman public key 

send_msg(angus_socket, angus_DH_public_bytes)

send_msg(angus_socket, angus_rsa_public_bytes)

send_msg(angus_socket, angus_signature)

print("[+] Confirmation: Your public keys and signature have been shared.")


# --------------------------------------------------------------------

# Step 5: Recieve other user's Diffie-Hellman key, RSA key, and signature
     # receiving keys in byte format, as well as signature, with recv_msg function to ensure full bytes are received

bobby_DH_public_bytes = recv_msg(angus_socket)

bobby_rsa_public_bytes = recv_msg(angus_socket)

bobby_signature = recv_msg(angus_socket)


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
    angus_socket.close()
    exit()


# wrapping of verificatioon of RSA signature in an explicit exception, raising exception, closing socket session, and exiting program upon verification failure
try:
    verify_rsa_signature(bobby_rsa_public_key, bobby_signature, bobby_DH_public_bytes)
except Exception as e3:
    print("[!] Error: Invalid signature. Connection terminated.")
    print(f"[!!] Details: {e3}")

    # upon verification failure
    angus_socket.close()
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
    angus_socket.close()
    exit()

shared_secret_key = calculate_shared_key(angus_DH_private, bobby_DH_public_key)

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

# Step 10: Sending of the nonce and ciphertext to the recipient -> Bobby then closing connection
    # again, utilising the connection on the socket joined earlier on the local host interface and open port (8888)
    # again, using send_msg function to ensure all bytes are sent and read

send_msg(angus_socket, nonce)

send_msg(angus_socket, ciphertext)

print("[+] Confirmation: Encrypted message successfully sent to Bobby.")

# explicitly closing session socket once the communication has been sent
print("[+] Session complete. Terminating communication.")
angus_socket.close()


# --------------------------------------------------------------------