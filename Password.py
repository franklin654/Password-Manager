import json
import os
import random
import string
from base64 import b64encode, b64decode
from tkinter import messagebox
from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Util.Padding import pad, unpad

pass_key = "Sai Sivakesh"


class Password:
    def __init__(self, web_site: str, user_name: str = None, num=False, password_strength="v"):
        self.__characters = string.ascii_lowercase + string.ascii_uppercase
        self.__numbers = string.digits
        self.__special_characters = ['*', '@', '$', '%', '_', ':', '.', '/', '^', '~', '>', '#', '(', ')', '<']
        self.__num = num
        self.password_strength = password_strength
        self.__password_key = pass_key
        self.web_site = web_site
        self.__user_name = user_name

    def __generate_aes(self):
        key: bytes = self.read_hash_file()
        cipher = AES.new(key=key, mode=AES.MODE_CBC)
        return cipher

    def __encrypt_and_store(self, password: bytes):
        cipher = self.__generate_aes()
        cipher_text = cipher.encrypt(pad(password, cipher.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(cipher_text).decode('utf-8')
        json_dict = {'iv': iv, 'web_site': self.web_site, 'cipher_text': ct, 'user_name': self.__user_name}
        with open('passwords\\' + self.web_site + '.json', 'w') as f:
            json.dump(json_dict, fp=f)

    def generate_password(self, length=8, n=4) -> str:
        pwd = ""
        if self.password_strength == "s":
            if self.__num:
                length -= n
                for i in range(n):
                    pwd += random.choice(self.__numbers)
            for i in range(length):
                pwd += random.choice(self.__characters)

        else:
            if length >= 10:
                ran = random.randint(3, 5)
            else:
                ran = random.randint(2, 3)
            if self.__num:
                length -= ran
                for i in range(ran):
                    if i % 2:
                        pwd += random.choice(self.__numbers)
                    else:
                        pwd += random.choice(self.__special_characters)
            else:
                length -= ran
                for i in range(ran):
                    pwd += random.choice(self.__special_characters)
            for i in range(length):
                pwd += random.choice(self.__characters)

        pwd = list(pwd)
        random.shuffle(pwd)
        password = ''.join(pwd)
        self.__encrypt_and_store(password.encode('utf-8'))
        return password

    def read_password(self):
        with open('passwords\\' + self.web_site + '.json', 'r') as f:
            json_obj = json.load(fp=f)

        iv = b64decode(json_obj['iv'].encode('utf-8'))
        ct = b64decode(json_obj['cipher_text'].encode('utf-8'))
        key = self.read_hash_file()
        cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
        user_name = json_obj['user_name']
        plain_text = unpad(cipher.decrypt(ct), cipher.block_size)
        return user_name, plain_text.decode('utf-8')

    @staticmethod
    def update_pass_key(new_hash: bytes):
        passphrase = Password.read_hash_file()
        files = os.listdir('passwords')
        for i in files:
            with open('passwords\\' + i, 'r') as f:
                json_obj = json.load(fp=f)
            iv = b64decode(json_obj['iv'].encode('utf-8'))
            ct = b64decode(json_obj['cipher_text'].encode('utf-8'))
            o_key = passphrase
            o_cipher = AES.new(o_key, mode=AES.MODE_CBC, iv=iv)
            plain_text = unpad(o_cipher.decrypt(ct), o_cipher.block_size)
            n_cipher = AES.new(new_hash, mode=AES.MODE_CBC, iv=iv)
            n_cipher_text = n_cipher.encrypt(pad(plain_text, n_cipher.block_size))
            ct = b64encode(n_cipher_text).decode('utf-8')
            iv = b64encode(n_cipher.iv).decode('utf-8')
            json_obj['iv'] = iv
            json_obj['cipher_text'] = ct
            with open('passwords\\' + i, 'w') as f:
                json.dump(json_obj, fp=f)
        Password.save_hash_to_file(new_hash)

    @staticmethod
    def save_hash_to_file(key: bytes):
        with open(file="hash.txt", mode="wb") as f:
            f.write(key)

    @staticmethod
    def change_pass_key(npk: str):
        hash_pk = Password.__generate_hash(npk)
        Password.update_pass_key(hash_pk)
        messagebox.showinfo(title="New Password", message="Master Key Successfully Changed", icon="info")

    @staticmethod
    def read_hash_file() -> bytes:
        try:
            with open(file="hash.txt", mode="rb") as f:
                key = f.read()
            return key
        except FileNotFoundError:
            passphrase = input("Enter your master password:")
            key = Password.__generate_hash(passphrase)
            Password.save_hash_to_file(key)
            return key

    @staticmethod
    def __generate_hash(passphrase: str) -> bytes:
        h_obj = SHA3_256.new()
        h_obj.update(bytes(passphrase, 'utf-8'))
        key: bytes = h_obj.digest()
        return key

    @staticmethod
    def validate_master_password(passphrase: str) -> bool:
        password_hash: bytes = Password.__generate_hash(passphrase)
        with open("hash.txt", "rb") as f:
            if password_hash == f.read():
                return True
            else:
                return False
