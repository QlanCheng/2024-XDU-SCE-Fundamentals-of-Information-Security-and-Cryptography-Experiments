import random
import math
def mod_mult(multiplier, base, addend, mod):
    result = 0
    base = base % mod
    while multiplier > 0:
        if (multiplier % 2) == 1:  # 如果 b 是奇数
            result = (result + base) % mod
        base = (base * 2) % mod
        multiplier //= 2

    result = (result + addend) % mod
    return result

def EEA(r0, r1):#eea算法，把r_i表示成r0和r1的线性组合
    if type(r0) != int or type(r1) != int:
        raise TypeError("arguments must be integer!  参数必须是整数")

    if r1 > r0:
        print("Warning! Normally, The second parameter should be smaller than the first parameter. ")

    s = [1, 0]#r0的系数
    t = [0, 1]#r1的系数
    q = []#商
    r = [r0, r1]#余数
    i = 1
    while True:
        i += 1
        r_i = r[i-2] % r[i-1]
        r.append(r_i)#余数
        q.append(r[i-2] // r[i-1])#商

        s_i = s[i-2] - q[i-2] * s[i-1]
        t_i = t[i-2] - q[i-2] * t[i-1]
        s.append(s_i)
        t.append(t_i)

        if r_i == 0:
            return r[i-1], s[i-1], t[i-1]

def is_primitive_generator(g, mod, factors_mod_minus_1):
    # 判断g是否是GF(p) p为质数 的本原元
    # factors_mod_minus_1为可迭代对象。装着p-1的所有质因子

    # 指数exp = (p - 1) / q
    # 对每一个q, 如果g 都满足：pow(g, exp, p) != 1   则g是生成元
    for q in factors_mod_minus_1:
        exp = int((mod - 1) / q)  # (p - 1) / q算出来是float型，pow只接受int参数

        if pow(g, exp, mod) == 1:
            return False
    return True

def find_generator(mod, known_factors_mod_minus_1=None):
    # 找一个生成元。一个就够了。
    # 需要的参数： p ：素数。  factors : p-1的一些已知大素数因子。应为可迭代对象
    # 如果有factors, 则需要分解 p-1 / factors
    # 找到p-1的全部素数因子q1, q2, q3 ··· qk 后。
    # 指数exp = (p - 1) / q
    # 对每一个q, 如果g 都满足：pow(g, exp, p) != 1   则g是生成元
    number = mod - 1  # 待分解的数

    if known_factors_mod_minus_1:
        for factor in known_factors_mod_minus_1:
            number = number / factor

    factors = prime_factors_decomposition(number=number)
    # prime_factors_decomposition会返回list, 例如分解4会返回[2,2].但我们不需要重复的因子。
    # 所以: 转换为集合，再转换为列表，以此去重
    if known_factors_mod_minus_1:
        factors.extend(known_factors_mod_minus_1)

    factors = list(set(factors))

    for g in range(2, mod):
        if is_primitive_generator(g, mod=mod, factors_mod_minus_1=factors):
            return g
    raise ValueError("未能找到本原元")

def is_probable_prime(n, repetitions=20, mode='fermat'):
    if type(n) != int or type(repetitions) != int:
        raise TypeError("N and Repetitions must be integer!  参数必须是整数")
    if mode not in ['miller_rabin', 'fermat']:
        raise ValueError("Mode must be 'miller_rabin' or 'fermat'")

    # 如果 n 是 2 或 3，返回 True
    if n == 2 or n == 3:
        return True
    # 如果 n 是 1 或者是偶数，返回 False
    if n == 1 or n % 2 == 0:
        return False

    import random
    if mode == 'miller_rabin':
        # 将 n-1 分解为 2^s * d，其中 d 是奇数
        s = 0
        d = n - 1
        while d % 2 == 0:
            d //= 2
            s += 1

        for i in range(repetitions):
            # 随机选择一个基 a
            a = random.randint(2, n - 2)
            x = pow(a, d, n)

            if x == 1 or x == n - 1:
                continue

            for j in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False

        return True
    else:
        for i in range(repetitions):
            a = random.randint(2, n - 2)
            gcd = EEA(n, a)[0]
            if gcd != 1:
                return False
            # 计算 a^(n-1) % n
            if pow(a, n - 1, n) != 1:
                return False
        return True

def prime_factors_decomposition(number):
    """返回 number 的所有质因数分解"""
    factors = []
    # 检查 2 作为因子
    while number % 2 == 0:
        factors.append(2)
        number //= 2
    # 检查奇数因子从 3 开始
    i = 3
    while i * i <= number:
        while number % i == 0:
            factors.append(i)
            number //= i
        i += 2
    # 如果剩下的 number 本身是质数
    if number > 1:
        factors.append(number)
    return factors

def bytes_to_integers(bytes_sequence, block_size):
    #作用是，把比特序列按block_size分组，每一组作为一个大整数。
    #返回一个列表，其中装着这些大整数
    #转换法则是，不足block_size的不补0。
    if type(bytes_sequence) not in [bytes, bytearray]:
        raise TypeError('第一个参数(比特序列)类型必须是bytes或者bytearray')

    integers = []
    for i in range(0, len(bytes_sequence), block_size):
        bytes_block = bytes_sequence[i:i + block_size]
        new_number = int.from_bytes(bytes_block, 'big')
        integers.append(new_number)

    return integers

def integers_to_bytes(integers, mode='ignore', block_size=510):
    #bytes_to_integers函数的逆变换
    #作用是： 把一个或多个大整数，拼接成一个大的字节序列。
    #返回值：bytearray类型

    #问题 1 ：
    #例如十进制的2，它可能由00000010转换而来; 也可能是由00000000 00000010转换而来; 或者若干个全0字节，最低字节是00000010转换而来
    #对待这种情况，有zero参数来控制，zero=ignore时,忽略全0字节。zero=reserve时,按Block_size，保留全0字节
    #问题 2 :
    #有时候block_size无法满足转换需求，例如block_size = 1时; 无法将65536用一个字节表示
    #解决方法: 发生这种错误时，会引发OverflowError， 捕获它，然后令block_size自适应+1，直到加到合适值
    #(一般情况下，需要+1的次数并不会很多)，也就是说，用户输入的block_size与真正需求的block_size绝大情况下都一样。


    bytes_sequence = bytearray(0)    #作为返回值，初始化为空的bytearray对象

    if mode == 'ignore':
        for number in integers:
            # 计算需要多少字节来表示这个十进制数 (每个字节8位)
            num_bits = number.bit_length()
            num_bytes = math.ceil(num_bits / 8)
            while True:
                try:
                    bytes_block = bytearray(number.to_bytes(length=num_bytes, byteorder='big'))
                    #to_bytes方法的返回类型是bytes，强制转换成bytearray
                    break
                except OverflowError:
                    num_bytes += 1
            bytes_sequence = bytes_sequence + bytes_block

    if mode == 'reserve':
        for number in integers:
            while True:
                try:
                    bytes_block = bytearray(number.to_bytes(length=block_size, byteorder='big'))
                    #to_bytes方法的返回类型是bytes，强制转换成bytearray
                    break
                except OverflowError:
                    print('overflow')
                    a = input('请查看提示')
                    exit(1)
            bytes_sequence = bytes_sequence + bytes_block

    return bytes_sequence

class ElGamalCipher():
    def __init__(self, public_key=None, private_key=None, generator=None, modulus=None):
        self.plaintext = None
        self.ciphertext = None
        args = [public_key, private_key, generator, modulus]

        if not any(args):  # 用户没有给出任何参数，需要生成密钥
            self.public_key, self.private_key, self.generator, self.mod = self.generate_keys()
        else:  # 用户给出两个或者三个参数,使用模式，无需产生密钥
            for arg in args:
                if arg and type(arg) != int:
                    raise TypeError('args must be integer')

            self.public_key = public_key
            self.private_key = private_key
            self.generator = generator
            self.mod = modulus

    @staticmethod
    def generate_keys():
        # 采用512bits 的 模数（质数p）
        # 素数p 要求: p-1有大素数因子q。所以先生成一个大质数q。验证 cq+1(c为正整数)是否是素数，如果是，则可以令p=cq+1
        # 大素数因子q 选取480bits - 482bits之间。不推荐也不支持修改。过小会导致密钥生成不出来。
        # 实验证明，不可以确定q而找c，根本找不到。
        # 应该随机生成c和q。而非确定q，随机生成c
        q_min = 2 ** 480
        q_max = 2 ** 482
        c_min = 2 ** 30
        c_max = 2 ** 31
        p_min = 2 ** 511
        p_max = 2 ** 512
        mod = 0  # 先声明一下mod，消掉该死的警告

        def find_q():
            while True:
                q = random.randint(q_min, q_max)
                if is_probable_prime(q, repetitions=25, mode='fermat'):
                    return q

        while True:
            # 选择合适的c 使的 cq+1 处于2**510 到 2**512之间
            q = find_q()
            c = random.randint(c_min, c_max)
            candidate = c * q + 1
            # 虽然通过限制c的范围，确保了candidate在合适范围内，但还是加一个冗余，保险起见。
            if p_min < candidate < p_max:
                if is_probable_prime(candidate, repetitions=25, mode='fermat'):
                    mod = candidate
                    print('mod is ready')
                    print(f'mod = {mod}')
                    print(f'mod = 2 * {q} + 1')
                    break
            else:
                continue
        # mod 已经选好
        # 接下来选取GF(mod)的生成元generator
        generator = find_generator(mod=mod, known_factors_mod_minus_1=[q])
        print('generator is ready')
        print(f'generator = {generator}')
        # 随机选取一个整数, 在区间(2, mod-2)内。作为私钥。
        # 计算 y = a**d mod p 作为公钥

        private_key = random.randint(2, mod-2)
        print(f'private_key = {private_key}')
        public_key = pow(generator, private_key, mod)
        print(f'public_key = {public_key}')
        print('keys are ready')
        return public_key, private_key, generator, mod

    def encrypt(self, block_size=63):
        k_min = 2**64
        # 依然是先把明文搞成大整数。
        plaintexts = bytes_to_integers(bytes_sequence=self.plaintext, block_size=block_size)
        ciphertext = []
        for plaintext in plaintexts:
            # 随机选择一个整数k 介于 2 和 p-2之间 （但实际上不能太小），计算出u
            k = random.randint(k_min, self.mod - 2)
            print(f'k = {k}')
            u = pow(self.public_key, k, self.mod)
            cipher_1 = pow(self.generator, k, self.mod)
            cipher_2 = mod_mult(u, plaintext, addend=0, mod=self.mod)
            ciphertext.append(cipher_1)
            ciphertext.append(cipher_2)
            print('ciphertext is ready')
            print(f'C1 = {cipher_1}, C2 = {cipher_2}')
        self.ciphertext = ciphertext

    def decrypt(self, mode='ignore', block_size=63):
        if mode not in ['ignore', 'reserve']:
            raise ValueError('mode必须是ignore或者reserve')

        integers = []
        for i in range(0, len(self.ciphertext), 2):
            cipher_1, cipher_2 = self.ciphertext[i], self.ciphertext[i+1]
            v = pow(cipher_1, self.private_key, self.mod)
            # 找到v的模self.mod乘法逆元
            v_reverse = EEA(self.mod, v)[2] % self.mod
            plaintext = mod_mult(v_reverse, cipher_2, addend=0, mod=self.mod)
            integers.append(plaintext)

        self.plaintext = integers_to_bytes(integers=integers, mode=mode, block_size=block_size)



if __name__ == '__main__':
    plaintext = 268934047525129207430358090155831774406988263017537886266459743124401877032780923870438637078936998897356703572131607069480172048042746
    plaintext = plaintext.to_bytes(length=(plaintext.bit_length() + 7) // 8, byteorder='big')

    cipher = ElGamalCipher()
    cipher.plaintext = plaintext
    cipher.encrypt()
    print(cipher.ciphertext)
    cipher.plaintext = None
    cipher.decrypt()
    print(cipher.plaintext)
    print(cipher.plaintext == plaintext)