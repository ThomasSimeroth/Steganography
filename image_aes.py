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

def aes_main(user_choice, filename):
    if user_choice == "E" or user_choice == "e":
        key = ("Enter the password: ")
        key = generate_key(key)
        init_vector = encrypt(filename, key)
        store_init_vector(filename, init_vector)
    elif user_choice == "D" or user_choice == "d":
        key = ("Enter the password: ")
        key = generate_key(key)
        iv_file_name = "iv_" + filename[10:]
        init_vector = load_init_vector(iv_file_name)
        decrypt(filename, key, init_vector)

        return "new_" + filename[10:]
    else:
        print("Incorrect input. Exiting...")