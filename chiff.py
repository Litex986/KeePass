from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA512
from Cryptodome.Protocol.KDF import HKDF
from Cryptodome.Random import random

class Crypt:
    def __init__(self, key1: str, key2: str) -> None:
        self.keys = HKDF(SHA512.new(key1.encode()).digest(), 32, SHA512.new(key2.encode()).digest(), SHA512, 3)
    
    def deriveKey(self, key: bytes, salt: str) -> list:
        return HKDF(SHA512.new(key).digest(), 32, salt.encode(), SHA512, 2)
    
    def encrypt(self, key: bytes, data: str) -> str:
        cipher_encrypt = AES.new(key, AES.MODE_CBC)
        return (cipher_encrypt.iv + cipher_encrypt.encrypt(data.encode() + (AES.block_size - len(data.encode()) % AES.block_size) * b'\0')).hex()
    
    def decrypt(self, key: bytes, data: str) -> str:
        iv = bytes.fromhex(data)[:AES.block_size]
        cipher_decrypt = AES.new(key, AES.MODE_CBC, iv)
        return cipher_decrypt.decrypt(bytes.fromhex(data)[AES.block_size:]).rstrip(b'\0').decode()

class KeyPass:
    def __init__(self) -> None:
        self.key_list = {}

    def openKey(self, key1: str, key2: str) -> None:
        self.aes = Crypt(key1, key2)
        try:
            file = [[j for j in i.split('/')] for i in self.aes.decrypt(self.aes.keys[0], open("aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2gdj1kUXc0dzlXZ1hjUSZhYl9jaGFubmVsPVJpY2tBc3RsZXk", 'r').read()).split('|')]
            if file != [['']]:
                for i in file:
                    self.key_list[i[0]] = {'Username': i[1], 'Password': i[2], 'Index': i[3]}
        except FileNotFoundError:
            self.saveKey()
        self.v2 = SHA512.new(key2.encode()).digest()
    
    def saveKey(self) -> None:
        a = self.aes.encrypt(self.aes.keys[0], '|'.join(['/'.join([i, self.key_list[i]['Username'], self.key_list[i]['Password'], self.key_list[i]['Index']]) for i in self.key_list.keys()]))
        open("aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2gdj1kUXc0dzlXZ1hjUSZhYl9jaGFubmVsPVJpY2tBc3RsZXk", 'w').write(a)
    
    def newKey(self, site: str, user: str, key: str) -> None:
        index = str(len(self.key_list))
        keys = self.aes.deriveKey(self.aes.keys[2], index)
        self.key_list[self.aes.encrypt(self.aes.keys[1], site)] = {'Username': self.aes.encrypt(keys[0], user), 'Password': self.aes.encrypt(keys[1], key), 'Index': index}
        self.saveKey()
    
    def genPass(self, lenght = 30) -> str:
        temp = random.sample("0123456789", int(lenght/5)) + random.sample("azertyuiopqsdfghjklmwxcvbn", int(lenght/5)) + random.sample("azertyuiopqsdfghjklmwxcvbn".upper(), int(lenght/5)) + random.sample("&é'(-è_çà)=~#[{|`^@]}<>?,.;/:§!¨£$€¤%ùµ*", int(lenght/5))
        random.shuffle(temp)
        return ''.join(temp)