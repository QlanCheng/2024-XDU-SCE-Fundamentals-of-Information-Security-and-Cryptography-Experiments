import random
from sympy import isprime
import itertools

class CustomError(Exception):
    def __init__(self, message, value1, value2, gcd):
        super().__init__(message)
        self.value1 = value1
        self.value2 = value2
        self.gcd = gcd

def EEA(r0, r1):#eea算法，把r_i表示成r0和r1的线性组合
    if type(r0) != int or type(r1) != int:
        raise TypeError("arguments must be integer!  参数必须是整数")
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


def process(a:list, m:list, e:CustomError):
    processed_a = a[:]
    processed_m = m[:]
    m1, m2, gcd = e.value1, e.value2, e.gcd
    idx1, idx2 = m.index(m1), m.index(m2)
    a1, a2 = a[idx1], a[idx2]

    if a1 % gcd != a2 % gcd:
        print('无解')
        print(f'{a1} mod {gcd} = {a1 % gcd}')
        print(f'{a2} mod {gcd} = {a2 % gcd}')
        exit(1)
    else:
        new_m = [gcd, m1//gcd, m2//gcd]
        new_a = [a1 % gcd, a1 % (m1//gcd), a2 % (m2//gcd)]

        # 清除原数据
        processed_a.remove(a1)
        processed_a.remove(a2)
        processed_m.remove(m1)
        processed_m.remove(m2)

        # 添加新数据
        processed_a.extend(new_a)
        processed_m.extend(new_m)
        return processed_a, processed_m


def Chinese_remainder_theorem(a:list, m:list):
    for i in range(len(m)):
        for j in range(i+1, len(m)):
            m_i, m_j = m[i], m[j]
            gcd = EEA(m_i, m_j)[0]
            if gcd != 1:
                raise CustomError(f'不互素 {m_i}, {m_j}', m_i, m_j, gcd)

    product = 1  #  所有模数的乘积。
    for num in m:
        product *= num
    M = [product//num for num in m]
    M_reverse = [EEA(m_num, M_num)[2] % m_num for M_num, m_num in zip(M, m)]

    # 开始计算结果
    buffer = 0
    for a_num, M_num, M_re_num in zip(a, M, M_reverse):
        buffer += a_num * M_num * M_re_num

    x = buffer % product

    # 把x代入每个原方程。
    for a_num, m_num in zip(a, m):
        assert x % m_num == a_num

    return x, product


def generate_coprime_numbers(t, n, k):
    """生成 n 个两两互素的整数 d_i，递增顺序"""

    def inner_function():
        coprimes = []
        lower_bound = 2 ** 500
        upper_bound = 2 ** 600
        while len(coprimes) < n:
            candidate = random.randint(lower_bound, upper_bound)
            # 两两互素
            if all(EEA(candidate, di)[0] == 1 for di in coprimes):
                coprimes.append(candidate)
        return sorted(coprimes)

    while True:
        coprimes = inner_function()
        N, M = 1, 1
        for i in range(t):
            N = N * coprimes[i]
        for i in range(t - 1):
            M = M * coprimes[-i]
        if N > k > M:
            print(coprimes)
            print(N)
            print(M)
            return coprimes

if __name__ == '__main__':
    t = int(input('输入t'))
    n = int(input('输入n'))
    k = 53823875121815031555991041726961963027167497087379606444752695810921446308620440784282908764903404381700859802589128088582231023318257395900650579969430836361568310072045989148202938122332018094970612150023975385103662839669401286231859032076966069321281804566076496995671875391401767723508755290586711966288915719170263680685765819809015089246767200303041035239107653221933068989117389227123695590846277200135849802429057524011609755858115850472691720432153190744237874436679626434222385571795646340

    d_values = generate_coprime_numbers(t, n, k)
    k_values = [k % di for di in d_values]

    for combination in itertools.combinations(range(n), t):
        di = [d_values[i] for i in combination]
        ki = [k_values[i] for i in combination]
        secret, mod = Chinese_remainder_theorem(ki, di)
        print(secret == k, ((secret % mod) == (k % mod)))




