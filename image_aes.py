from Crypto.Cipher import AES

def encrypt(filename, key):
    aes_encryptor = AES.new(key, AES.MODE_CBC)
    init_vector = aes_encryptor.iv


    return init_vector

def decrypt(filename, key, init_vector):


def generate_key(key_text):


def main():
    

main()