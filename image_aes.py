from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

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

def main():
    file_to_e = "testtext"
    file_to_d = "encrypted_testtext"
    key = "password"
    init_vector = encrypt(file_to_e, generate_key(key))
    decrypt(file_to_d, generate_key(key), init_vector)

main()