"""
The purpose of this file and code is to be the core file or cryptographic engine of the Diffie-Hellman Key Exchange, utilising ephemeral Diffie-Hellman (DHE).
Each session generates fresh private keys, public keys, and shared secret, to ensure perfect forward secrecy and preventing key re-use attacks.

This file will focus on five core functions that:
    1. generate the parameters 
    2. generate the secret key for each user 
    3. generate the public key of each user (in byte form), 
    4. reverse serialisation of other user's public key from byte form back into the key
    5. compute the shared key
    """

# Student ID: 36305138
# Student Name: Alexander McNeill

# imports: 
    # import the dh module from the python cryptography library for secure parameters
from cryptography.hazmat.primitives.asymmetric import dh
    # import the serialisation module from python cryptography library to convert public key into bytes, as well as reverse serialisation for shared key calculation
from cryptography.hazmat.primitives import serialization


# Generate reusable Diffie-Hellman parameters, safe prime and generator -> amended to fixed from dynamic to resolve technical issues with paramater generation

# 2048-bit mod p prime (safe prime) -> written in hexadecimal (base-16) formatting for readability, with triple quote strings holding the hex digits
p = int("""FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1
29024E088A67CC74020BBEA63B139B22514A08798E3404DD
EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245
E485B576625E7EC6F44C42E9A63A36210000000000090563
""".replace("\n", ""), 16)

# generator, g = 2 as previously used in dynamic implementation
g = 2


# turn parameters p and g into Diffie-Hellman parameter objects for the dh cryptography library to use
parameters = dh.DHParameterNumbers(p, g).parameters()



# function to generate the private key - heavy lifting completed by the dh cryptography module to produce ephemeral private keys

def generate_private_key():
    """The purpose of this function is to generate and return the private key for each user."""

    return parameters.generate_private_key()


# function to generate the public key in bytes - heavy lifting done by the serialization module to produce a standardised public key output in bytes

def get_public_key_bytes(private_key):
    """ The purpose of this function is to generate and return the public key in byte form for transmission for each user."""

    public_key = private_key.public_key()

    # return public key as bytes in PEM encoding: base64 encoding text, wrapped in a header and footer, standardised, and compatible with Wireshark for demonstration
    return public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)


# function to obtain receipients public key from byte form - again utilising the serialisation module for the reverse serialisation of the public key

def convert_bytes_to_key(others_bytes):
    """ The purpose of this function is to obtain the other user's public key from byte form."""

    return serialization.load_pem_public_key(others_bytes)


# function to compute the shared key, using the private key and other user's public key - utilising cryptography dh module to handle the conversion

def calculate_shared_key(private_key, others_public_key):
    """ The purpose of this function is to calculate the shared key."""

    return private_key.exchange(others_public_key)






