"""
The purpose of this code file is to act as the user receiving the message and to format the connection to the socket, generation of keys, the verification of sender signature,
the computation of the shared secret, derivation of the AES key, the reception of the encrypted message, and finally to decrypt and provide the ciphertext in plaintext for the 
recipient.

Key tasks include:
    1. RSA identity key generation -> for authentication.
    2. Diffie-Hellman key generation -> produces the shared secret and facilitates the key exchange.
    3. Receiving other user's Diffie-Hellman public key and RSA signature.
    4. Verification of the other user's signature -> authenticating user is who they say they are.
    5. Sending the Diffie-Hellman public key and signature.
    6. Deriving the shared AES key -> for the ensurance of confidentiality and integrity.
    7. Receiving and decrypting the ciphertext back into plaintext.

In structuring this project, I have utilised three files that act as different engines (dh_engine (Diffie-Hellman), identity_authentication (RSA), and 
crypto_confidentiality_integrity (AES-GCM)), and as such, will import the functions for execution.
"""

# Student ID: 36305138
# Student Name: Alexander McNeill


# Imports:
    # import socket module in order to establish a connection for demonstration over the network
import socket
    # import functions from the identity_authentication code file for the generation and verification of RSA key and verification of signature
from identity_authentication import generate_rsa_identity_key, generate_public_identity_bytes, convert_public_identity_key, sign_authentication_data, verify_rsa_signature
    # import functions from the dh_engine code file for the generation of Diffie-Hellman key pair and the computation of the shared secret
from dh_engine import generate_private_key, get_public_key_bytes, convert_bytes_to_key, calculate_shared_key
    # import functions from the crypto_confidentiality_integrity code file for the generation of the SHA256 AES-GCM key and decryption of AES-GCM ciphertext to plaintext
from crypto_confidentiality_integrity import convert_sharedsecret_symmetric_key, decrypt_ciphertext_plaintext




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

# Step 1: Generation of Bobby's RSA identity keys for identity authentication -> private key and public key in bytes form
bobby_rsa_private = generate_rsa_identity_key()

bobby_rsa_public_bytes = generate_public_identity_bytes(bobby_rsa_private)


# --------------------------------------------------------------------


# Step 2: Generate Bobby's Diffie-Hellman key pair -> again, private key and public key in byte format
bobby_DH_private = generate_private_key()

bobby_DH_public_bytes = get_public_key_bytes(bobby_DH_private)


# --------------------------------------------------------------------

# Step 3: Create connection to the network socket for Bobby
    # This is done first for Bobby as they will be the one receiving the communication and have to be ready to receive the message

bobby_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # using AF_INET == Address family is IPv4 addresses
    # SOCK_STREAM is using a TCP socket stream based communication

bobby_socket.bind(("localhost", 8888))
    # binds the socket connection to the local host interface on port 8888 -> 127.0.0.1:8888 Bobby is waiting here

bobby_socket.listen(1)
    # turns bobby into a receiver -> Bobby is 'listening' for incoming communications, ready to receive

print("[+] Welcome Bobby! You are connected to the network. Waiting for connection from other users.")

session_socket, user_address = bobby_socket.accept()    # <-- Bobby is waiting here until another user has connected to the socket (session)
print("[+] Angus has connected from:", user_address)

print("[+] Secure session established. Beginning key exchange...")

# --------------------------------------------------------------------

# Step 4: Receiving other user's information -> Diffie-Hellman public key (bytes), RSA public key (bytes), and user's signature for verification
    # receiving keys in byte format, as well as signature, utilsing recv_msg function
    # raising exception and message if verification fails

angus_DH_public_bytes = recv_msg(session_socket)

angus_rsa_public_bytes = recv_msg(session_socket)

angus_signature = recv_msg(session_socket)

# wrapping conversion of Angus' rsa public key bytes into an exception for demonstration of robustness
    # convert Angus' rsa public key bytes into the public key

try:
    angus_rsa_pub_key = convert_public_identity_key(angus_rsa_public_bytes)
except Exception as e:
    print("[!] Error: Invalid RSA public key received. Connection terminated")
    print(f"[!!] Details: {e}")
    
    # upon verification failure, close connection
    session_socket.close()
    exit()

# --------------------------------------------------------------------

# Step 5: Verify Angus' signature
    # verifying Angus' sgnature by calling verify_rsa_signature function with Angus' rsa public key, signature, and Diffie-Hellman public key in bytes to confirm identity

# wrapping verification of RSA signature in explicit exception, raising exception, closing socket session, and exiting program upon failure
try:
    verify_rsa_signature(angus_rsa_pub_key, angus_signature, angus_DH_public_bytes)
except Exception as e1:
    print("[!] Error: Invalid signature. Connection terminated.")
    print(f"[!!] Details: {e1}")

    # upon verification failure
    session_socket.close()
    exit()

# if rsa signature verified -> print authentication confirmation
print("[+] Angus' identity and Diffie-Hellman key has been authenticated.")
    # if not authenticated, the program will run an exception, as programmed through identity_authentication and use of cryptography library


# --------------------------------------------------------------------

# Step 6: Bobby sends their Diffie-Hellman key, RSA key, and signature for verification by Angus
    # Bobby to send public bytes version of Diffie-Hellman and RSA public keys, as well as Bobby's signature -> using send_msg function

bobby_signature = sign_authentication_data(bobby_rsa_private, bobby_DH_public_bytes)


send_msg(session_socket, bobby_DH_public_bytes)

send_msg(session_socket, bobby_rsa_public_bytes)

send_msg(session_socket, bobby_signature)

print("[+] Confirmation: Your public keys and signature have been shared.")


# --------------------------------------------------------------------

# Step 7: Compute the shared secret
    # Bobby to compute the shared secret from Angus' Diffie-Hellman public key, post byte conversion back to key, and Bobby's private Diffie-Hellman key

# wrapping Diffie-Hellman public key conversion in explicit exception, to protect against malformed key
try:
    angus_DH_public_key = convert_bytes_to_key(angus_DH_public_bytes)
except Exception as e5:
    print("[!] Error: Invalid Diffie-Hellman public key received. Connection terminated.")
    print(f"[!!] Details: {e5}")

    # upon verification failure, close connection
    session_socket.close()
    exit()

shared_secret_key = calculate_shared_key(bobby_DH_private, angus_DH_public_key)

print("[+] Confirmation: The shared secret has been calculated.")


# --------------------------------------------------------------------

# Step 8: Generate the AES encrypted shared secret key
    # Take the shared secret generated in step 7 and hash it in SHA256 to generate the key

aes_shared_key = convert_sharedsecret_symmetric_key(shared_secret_key)

print("[+] Confirmation: The shared key has been generated.")


# --------------------------------------------------------------------

# Step 9: Receiption of the encrypted message
    # once the shared secret, keys, and verification/authentication has occured, the other user can then send the encrypted message (ciphertext) and nonce

nonce = recv_msg(session_socket)

ciphertext = recv_msg(session_socket)

print("[+] New message received!")


# --------------------------------------------------------------------

# Step 10: Decrypt and print the plaintext message
    # decrypting the ciphertext utilisng the AES shared key, nonce, and ciphertext and decode function
    # using decode to decode the byte format plaintext message into string, word, format

# wrapping AES-GCM decryption in explicit exception to raise exception, termination session, and close program if ciphertext has been tampered with
try:
    plaintext = decrypt_ciphertext_plaintext(aes_shared_key, nonce, ciphertext)
except Exception as e6:
    print("[!] Error: Potential malformed ciphertext. Connection terminated.")
    print(f"[!!] Details: {e6}")

    # upon verification failure, close connection
    session_socket.close()
    exit()

print("[+] New message decrypted!")
print("[+] Decrypted message from Angus:", plaintext.decode())


# --------------------------------------------------------------------

# Step 11: close of socket and connection upon completion of communication
    # explicitly closing the socket session upon receipt of message to securely end communication

print("[+] Communication recieved and complete. Session terminated.")
session_socket.close()