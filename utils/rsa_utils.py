# -*- coding: utf-8 -*-
import rsa
from base64 import b64encode, b64decode


class RsaCrypto(object):
    def __init__(self, private_key_file, public_key_file):
        self.__private_key_file = private_key_file
        self.__public_key_file = public_key_file
        self.__rsa_pri = self.rsa_pri
        self.__rsa_pub = self.rsa_pub

    @classmethod
    def gen_key_pair(self, pri_key_name, pub_key_name):
        pub_key, pri_key = rsa.newkeys(1024)
        self.save_file(pri_key, pri_key_name)
        self.save_file(pub_key, pub_key_name)

    @staticmethod
    def save_file(key_obj, key_file_name):
        key = key_obj.save_pkcs1()
        with open(key_file_name, 'w') as f:
            f.write(key)

    @property
    def rsa_pub(self):
        with open(self.__public_key_file) as public_file:
            p = public_file.read()
            pub_key = rsa.PublicKey.load_pkcs1(p)
            return pub_key

    @property
    def rsa_pri(self):
        with open(self.__private_key_file) as private_file:
            p = private_file.read()
            pri_key = rsa.PrivateKey.load_pkcs1(p)
            return pri_key

    def encrypt(self, msg, pub=True):
        key = self.__rsa_pri
        if pub:
            key = self.__rsa_pub
        return b64encode(rsa.encrypt(msg, key))

    def decrypt(self, crypto, pri=True):
        key = self.__rsa_pub
        if pri:
            key = self.__rsa_pri
        return rsa.decrypt(b64decode(crypto), key)

    def sign(self, msg):
        return b64encode(rsa.sign(msg, self.__rsa_pri, 'SHA-1'))

    def verify(self, msg, sign):
        return rsa.verify(msg, b64decode(sign), self.__rsa_pub)


if __name__ == '__main__':
    msg = '韩能放'
    private_key_file, public_key_file = 'rsa/rsa_private_key.pem', 'rsa/rsa_public_key.pem'
    # RsaCrypto.gen_key_pair(private_key_file, public_key_file)  # 1.生成公私钥
    rsa_crypto = RsaCrypto(private_key_file, public_key_file)

    # 2.公钥加密、私钥解密
    # crypto = rsa_crypto.encrypt(msg)
    # txt = rsa_crypto.decrypt(crypto)
    # print crypto
    # print txt

    # 3.用私钥签名认真、再用公钥验证签名
    # signature = rsa_crypto.sign(msg)
    # print signature
    # print rsa_crypto.verify(msg, signature)