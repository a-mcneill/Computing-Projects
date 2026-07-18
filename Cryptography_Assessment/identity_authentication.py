"""
The purpose of this file and code is to produce the ability for users to generate long-term identity keys utilising the RSA cryptosystem.
This will allow the users to sign their Diffie-Hellman public keys and data exchanged, allowing them to verify the other user's signature.

This program is the implementation of the Authentication layer of the CIA triad to ensure the authenticity of communication between users and allows the users to prove that their
Diffie-Hellman public keys truly came from the specific user.

This program will focus on four (4) key tasks:
    1. RSA Key generation.
    2. Public Key Serialisation.
    3. Signing of data using RSA key
    4. Verification of RSA signature
"""

# Student ID: 36305138
# Student Name: Alexander McNeill

# imports:
    # import rsa with padding to add randomness, prevent signature forgery, and ensure RSA signature operation is secure -> padding is the tamper proof wrapper on RSA
from cryptography.hazmat.primitives.asymmetric import rsa, padding
    # import serialisation and hashing for the serialisation and use of PEM encoding of public RSA key & hash for the signining of data for authentication and verification
from cryptography.hazmat.primitives import serialization, hashes


# generate RSA private identity key for user
def generate_rsa_identity_key():
    """The purpose of this function is to generate and return a long-term RSA provate key for a user's identity, which is then used to sign Diffie-Hellman public keys.
        65537 is a Fermat prime chosen for the public exponent of the RSA operation to ensure attack resistant exponent for RSA exponentiation efficiency and is considered
        industry standard."""

    rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    return rsa_private_key


# generate the public part of the RSA private identity key in bytes -> utilising PEM encoding for standardised public key output, as used in dh_engine
def generate_public_identity_bytes(rsa_private_key):
    """The purpose of this function is to generate and return the public part of the identity key in PEM econded bytes, for transmission to the other user."""

    rsa_public_key = rsa_private_key.public_key()

    # return the public key aspect of the RSA identity key in PEM econded bytes format using serialisation
    return rsa_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)


# convert PEM encoded bytes back into a usable RSA public key object -> used to verify signatures of the other users but requires reverse serialisation of public key
def convert_public_identity_key(pem_bytes):
    """The purpose of this function is to convert a RSA public key encoded in bytes back into a usable public key for signature verification, utilising reverse serialisation 
        of the public key bytes."""
    
    return serialization.load_pem_public_key(pem_bytes)


# function to sign data utilising the users RSA private key, binding the data to the user's identity -> utilising padding (security wrapper - PKCS1v15 scheme) 
# & SHA256 hash for authentication
def sign_authentication_data(rsa_private_key, data: bytes):
    """The purpose of this function is to sign data, inc Diffie-Hellman public key and content, with the user's private identity key to bind the data to the user's identity."""

    user_signature = rsa_private_key.sign(data, padding.PKCS1v15(), hashes.SHA256())

    return user_signature 


# function to verify the signature, utilising the user's RSA public key, signature, and data -> again, using padding and SHA256 hash to ensure the signature hash matches
    # if signatures do not match, utilising cryptography library, it will raise an invalid signature exception stating that the signatures do not match
def verify_rsa_signature(rsa_public_key, user_signature: bytes, data: bytes):
    """The purpose of this function is to verify the signature on the data sent utilising the sender's RSA public key 
        -> raising an exception if the verification fails without requiring a function return value using crypto library."""

    rsa_public_key.verify(user_signature, data, padding.PKCS1v15(), hashes.SHA256())


    

