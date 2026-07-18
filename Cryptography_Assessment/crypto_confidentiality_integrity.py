"""
The purpose of this file and code is to implement the cryptographic confidentiality and authentication layer on top of the Diffie-Hellman key exchange, to ensure the secure
encryption and decryption of messages.

Utilising the Advanced Encryption Standard (AES) in Galois Counter Mode (AES-GCM) for symmetric encryption, the function will take the Diffie-Hellman shared secret, derive a 
symmetric key, and allow for the encryption and decryption of messages, using AES-CGM and a randomly generated nonce.

Key tasks:
    1. Generate a symmetric key from the Diffie-Hellman shared secret,
    2. Encrypt data using the AES-GCM encryption method.
    3. Decrypt data using the AES-GCM and detect if the data has been tampered.
"""

# Student ID: 36305138
# Student Name: Alexander McNeill


# imports:
    # import hashes module from cryptography library for use in SHA256 Diffie-Hellman shared secret symmetric key
from cryptography.hazmat.primitives import hashes
    # import AESGCM module from crypto library -> this is how I will encrypt and decrypt plaintext using the shared secret key
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    # import OS in order to generate a 96-bit (12 byte) nonce for the encryption of plaintext and also decryption using AES-GCM method and mode -> 96-bit as recommended for AES-GCM nonce
import os


# function to derive a 256-bit shared symmetric key from Diffie-Hellman shared secret utilising SHA256 hashing, ensuring a fixed-length for AES-GCM
def convert_sharedsecret_symmetric_key(shared_secret: bytes) -> bytes:
    """ The purpose of this function is to take the Diffie-Hellman shared secret in byte form, hash it using SHA256, and return it as a 32 byte key to then use for 
        encryption/decryption."""

    # define hash algorithm
    hash_func = hashes.Hash(hashes.SHA256())
    # use update to feed shared_secret into hash algo
    hash_func.update(shared_secret)
    # output hashed shared_secret as a key
    key = hash_func.finalize()

    return key


# function to encrypt plaintext using key and plaintext through AES-GCM encryption and os random nonce to produce the ciphertext
def encrypt_plaintext_ciphertext(key: bytes, plaintext: bytes):
    """The purpose of this function is to encrypt plaintext messages using the AES-GCM encryption method and mode in order to produce and return the cipher text.
        Taking the key derived in convert_shared_secret to encrypt plaintext alongside the use of a 96-bit nonce to produce the ciphertext."""
    
    # set up of encryption algorithm, key and nonce
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce -> 12 bytes

    # convert plaintext to ciphertext with alrogrithm/key and nonce -> return nonce and ciphertext
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    return nonce, ciphertext


# function to decrypt ciphertext using the key and nonce to convert back into plaintext -> raises excpetion if the ciphertext or tag has been modified, indicating integrity
    # and/or authentication failure
def decrypt_ciphertext_plaintext(key: bytes, nonce: bytes, ciphertext: bytes):
    """The purpose of this function is to decrypt the ciphertext message back into plaintext message, again utilising the key, AES-GCM, and nonce to return plaintext.
        Raises an exception if the ciphertext or tag has been modified, indicating integrity/authentication failure."""
    
    # setup of decryption algorithm, key -> then decrypting ciphertext with algo, key, and nonce, returning plaintext message
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    return plaintext
