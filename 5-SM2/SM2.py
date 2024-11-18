import random
import hashlib
from EllipticCurve import *
from utils import *

class SM2Cipher:
    def __init__(self, private_key: int=None, public_key: EllipticCurvePoint=None):
        self.G = G  # G定义在EllipticCurve.py， G里包含了椭圆曲线参数和生成元
        self.private_key = private_key
        self.public_key = public_key  # 应当是接收方的公钥
        self.h = 1  # 设置余因子为1，椭圆曲线的阶本身就是素数
        print(self.G)

    @staticmethod
    def generate_keys():
        private_key = random.randint(1, G.n - 1)
        public_key = private_key * G  # 是一个点
        return private_key, public_key

    def hash(self, data:bytes):
        sha256 = hashlib.new('sha256')
        sha256.update(data)
        return sha256.digest()

    def KDF(self, Z:EllipticCurvePoint, bytes_len):
        """KDF算法，生成和明文一样长的子密钥"""
        Z_bytes = Z.to_bytes()
        # 用于存储派生出的密钥
        result = b''

        i = 1  # 计数器 i
        while len(result) < bytes_len:
            # 将 Z 和计数器 i 拼接，作为 KDF 输入
            counter_data = Z_bytes + i.to_bytes(4, byteorder='big')
            # 计算 SHA256 哈希值
            hash_value = self.hash(counter_data)  # 使用 SHA-256
            result += hash_value  # 将哈希值拼接到结果中
            i += 1
        # 截取到需要的字节长度
        return result[:bytes_len]  # 返回派生密钥

    def encrypt(self, plain_text:bytes):
        k = random.randint(1, self.G.n - 1)  # 生成一个随机数
        cipher1 = k * self.G
        cipher1_bytes = cipher1.to_bytes()

        if (self.h * self.public_key).infinity:
            raise ValueError('S是无穷远点')

        Z = k * self.public_key
        sub_key = self.KDF(Z, len(plain_text))

        # 把 明文 和 sub_key按位异或， 在KDF里已经确保了sub_key和plain_text是长度一样的。
        cipher2_bytes = xor_bytes(plain_text, sub_key)
        x2My2 = Z.x.to_bytes(32, byteorder='big') + plain_text + Z.y.to_bytes(32, byteorder='big')
        cipher3_bytes = self.hash(x2My2)

        result = cipher1_bytes + cipher2_bytes + cipher3_bytes
        print(len(cipher1_bytes), len(cipher2_bytes), len(cipher3_bytes))
        return result

    def decrypt(self, cipher_text):
        # 取出三段
        cipher1_bytes, cipher2_bytes, cipher3_bytes = split_bytes(cipher_text)
        cipher1 = EllipticCurvePoint.from_bytes(cipher1_bytes)  #  这是个点对象

        if (self.h * cipher1).infinity:
            raise ValueError('S是无穷远点')

        Z = cipher1 * self.private_key
        sub_key = self.KDF(Z, len(cipher2_bytes))
        message = xor_bytes(cipher2_bytes, sub_key)
        x2My2 = Z.x.to_bytes(32, byteorder='big') + message + Z.y.to_bytes(32, byteorder='big')
        u = self.hash(x2My2)
        if u != cipher3_bytes:
            raise ValueError("u 不等于 cipher3")

        return message

if __name__ == '__main__':
    private_key, public_key = SM2Cipher.generate_keys()
    print(private_key, public_key)
    Cipher = SM2Cipher(private_key, public_key)

    message = "To me, you will be unique in all the world. To you, I shall be unique in all the world. "

    message = message.encode('utf-8')
    print("打印原始明文（已编码）：")
    print(message)

    ciphertext = Cipher.encrypt(message)
    print('打印密文：')
    print(ciphertext)
    message_recovered = Cipher.decrypt(ciphertext)
    print('打印解密后的明文（已解码）')
    print(message_recovered.decode('utf-8'))