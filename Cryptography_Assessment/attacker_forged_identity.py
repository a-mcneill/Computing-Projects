"""
The purpose of this code file is to act as an attacker script to demonstrate the robustness of my Diffie-Hellman Key Exchange implementation. This attacker script does this
by attempting to impersonate Angus, the user connecting to Bobby and sending a message, sending a forged identity during the authentication process.

The attacker connects to Bobby and sends a deliberately malformed Diffie-Hellman public key, RSA public key, and an invalid signature, in order to simulate a foregd identity
and test whether Bobby correctly rejects the unauthenticated user or tampered handshake data.

As a secure system must never accept invalid public keys or signatures, in this test, Bobby detects the malformed public keys and raises a cryptographic exception, safely 
terminationg the session.

This confirms the robustness properties:
    - Authentication robustness - rejects forged identities
    - Input vlaidation - detects malformed RSA and Diffie-Hellman key material
    - Error handling - cryptographic exceptions are caught safely
    - Secure failure - the connection is terminated cleanly
    - Resistance to malformed keys
    - Resistance to forged identities.

In this test case, the attacker replaces Angus entirely and demonstrates that the protocol fails safely when presented with an invalid or malicious handshake data. 
"""

# Student ID: 36305138
# Student Name: Alexander McNeill


# Imports:
    # import socket module in order to establish a connection for demonstration over the network
import socket
    # import os in order to generate random bytes for Diffie-Hellman and RSA key generation, as well as signature
import os


# implementation of send_msg function, to send the fraudulent keys and signature
def send_msg(socket, data: bytes):
    """The purpose of this function is to send a 4-byte big-endian length prefix followed by the raw data, ensuring the receiver knows exactly how many bytes to read.
        Differs from previous use in Bobby and Angus, as now utilising function for attacker testing."""

    length = len(data).to_bytes(4, 'big')   # using big-endian 4 byte length
    socket.sendall(length)
    socket.sendall(data)


# --------------------------------------------------------------------

# Create attacker socket connection
    # using AF_INET == Address family is IPv4 addresses
    # SOCK_STREAM is using a TCP socket stream based communication

attacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

attacker_socket.connect(("127.0.0.1", 8888))    # using localhost ip rather than 'localhost' as an attacker would


# --------------------------------------------------------------------

# Create fake Diffie-Hellman and RSA keys, and fake signature
    # utilising os.urandom to generate random 256-byte fake keys and signature
    # 256-bytes chosen as it matches the typical RSA 2048 key size
    # utilising send_msg to send the fake keys and signature as generated

# fake Diffie-Hellman + send_msg
fake_dh_key = os.urandom(256)
send_msg(attacker_socket, fake_dh_key)

print("[+] Attacker: Fake Diffie-Hellman key sent.")

# fake RSA key + send msg
fake_rsa_key = os.urandom(256)
send_msg(attacker_socket, fake_rsa_key)

print("[+] Attacker: Fake RSA key sent.")

# fake signature + send_msg
fake_sig = os.urandom(256)
send_msg(attacker_socket, fake_sig)

print("[!] Attacker: Fake Signature sent.")


# --------------------------------------------------------------------

# close connection -> attacker finished attack

attacker_socket.close()

print("[!] Attack Complete.")
print("[!!A] Expected Result: Bobby should reject this signature and terminate the session.")