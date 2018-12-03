import os, random, struct
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def encrypt(the_key, file_name):
    BlockSize = 64 * 1024
    outputFile = "(encrypted)" + file_name + '.enc'
    file_size = str(os.path.getsize(file_name))
    IV = ""
    for i in range(16):
        IV = IV + chr(random.randint(0, 0x7F))
    print(len(IV.encode("utf8")))
    print(IV)
    #IV = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(the_key, AES.MODE_CBC, IV.encode("utf8"))
    with open(file_name, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(file_size.encode('utf8'))
            outfile.write(IV.encode("utf8"))
            while True:
                chunk = infile.read(BlockSize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' '.encode("utf8") * (16 - (len(chunk) % 16))
                outfile.write(encryptor.encrypt(chunk))

def decrypt(the_key, file_name):
    chunksize = 64 * 1024
    outputFile = "newtesttext" #+ file_name[11:]
    if not outputFile:
        outputfile = os.path.splitext(file_name)[0]
    with open(file_name, 'rb') as infile:
        IV = ""
        for i in range(16):
            IV = IV + chr(random.randint(0, 0x7F))
        file_size = len(infile.read())
        infile.seek(0)
        decryptor = AES.new(the_key, AES.MODE_CBC, IV.encode("utf8"))
        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    while len(chunk) % 16 != 0:
                        chunk += " ".encode("utf8")
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(file_size)

def getthe_key(password):
    hash = SHA256.new(password.encode('utf-8'))
    return hash.digest()

def Main():
    userinput = "E"#input("Please type E to encrypt the file or D to decrypt the file: ")
    #if userinput == 'E' or userinput == 'e':
    file_name = "testtext"#"example3"#input("Please type the file name to encrypt: ")
    password = "password"#input("Please enter a password: ")
    hashedpw = getthe_key(password)
    encrypt(hashedpw, file_name)
    print("The file hase been encrypted.")
    #elif userinput == 'D' or userinput == 'd':
    file_name = "(encrypted)testtext.enc"#input("Please type the file name to decrypt: ")
    #password = input("Please enter a password: ")
    #hashedpw = getthe_key(password)
    decrypt(hashedpw, file_name)
    print("The file is decrypted.")
    #else:
    #    print("Please select a valid option.")

if __name__ == '__main__':
    Main()