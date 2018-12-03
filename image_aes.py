from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from image_encoder import *

def encrypt(filename, key):
    AES_BLOCK_SIZE = 16

    aes_encryptor = AES.new(key, AES.MODE_CBC)
    init_vector = aes_encryptor.iv
    encrypted_file = "encrypted_" + filename

    with open(filename, 'rb') as infile:
        with open(encrypted_file, 'wb') as outfile:
            chunk = infile.read(AES_BLOCK_SIZE)
            while len(chunk) > 0:
                if len(chunk) % 16 == 0:
                    outfile.write(aes_encryptor.encrypt(chunk))
                else:
                    outfile.write(aes_encryptor.encrypt(pad(chunk, AES_BLOCK_SIZE)))
                
                chunk = infile.read(AES_BLOCK_SIZE)

    return init_vector

def decrypt(filename, key, init_vector): 
    AES_BLOCK_SIZE = 16

    aes_decryptor = AES.new(key, AES.MODE_CBC, init_vector)
    decrypted_file = "new_" + filename[10:]

    with open(filename, 'rb') as infile:
        with open(decrypted_file, 'wb') as outfile:
            chunk = infile.read(AES_BLOCK_SIZE)
            while len(chunk) > 0:
                outfile.write(aes_decryptor.decrypt(chunk))
                chunk = infile.read(AES_BLOCK_SIZE)
            

def generate_key(key_text):
    while len(key_text) < 16:
        key_text += key_text
    return key_text[:16].encode("utf8")

def load_init_vector(iv_file):
    with open(iv_file, 'rb') as outfile:
        init_vector = outfile.read()

    return init_vector

def store_init_vector(filename, init_vector):
    iv_file = "iv_" + filename

    with open(iv_file, 'wb') as outfile:
        outfile.write(init_vector)

def main():
    user_choice = input("Enter 'E' to encrypt or 'D' to decrypt: ")
    if user_choice == "E" or user_choice == "e":
        file_to_e = input("Enter the filename to encrypt: ")
        key = ("Enter the password: ")
        key = generate_key(key)
        init_vector = encrypt(file_to_e, key)
        store_init_vector(file_to_e, init_vector)
    elif user_choice == "D" or user_choice == "d":
        file_to_d = input("Enter the filename to decrypt: ")
        key = ("Enter the password: ")
        key = generate_key(key)
        init_vector = input("Enter the filename of the initialization vector: ")
        init_vector = load_init_vector(init_vector)
        decrypt(file_to_d, key, init_vector)
    else:
        print("Incorrect input. Exiting...")

main()