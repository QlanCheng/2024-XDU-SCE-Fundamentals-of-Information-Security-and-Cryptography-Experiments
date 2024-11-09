import random
import math
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

def is_probable_prime(n, repetitions=20, mode='fermat'):
    """

    :param n: 要检验的数
    :param repetitions: 重复检验的次数
    :param mode: 方法，如fermat或millar-rabin
    :return: (bull值, 结果为此bull值的概率)
    """
    if type(n) != int or type(repetitions) != int:
        raise TypeError("N and Repetitions must be integer!  参数必须是整数")
    if mode not in ['miller_rabin', 'fermat']:
        raise ValueError("Mode must be 'miller_rabin' or 'fermat'")

    # 如果 n 是 2 或 3，返回 True
    if n == 2 or n == 3:
        return True, 1
    # 如果 n 是 1 或者是偶数，返回 False
    if n == 1 or n % 2 == 0:
        return False, 1

    if mode == 'fermat':
        for i in range(repetitions):
            a = random.randint(2, n - 2)
            gcd = EEA(n, a)[0]
            if gcd != 1:
                print(f'{a}是此数的一个因子')
                return False, 1
            # 计算 a^(n-1) % n
            if pow(a, n - 1, n) != 1:
                print(f'pow({a}, n - 1, n) != 1, 其结果为{pow(a, n - 1, n)}')
                return False, 1

        return True, (1-pow(2, -repetitions))

if __name__ == '__main__':
    numbers = [292491634125649724706298578583067489755302040058427247409073711608052500836509665659352490454953094982884551835361337799480001778313819979868070513149907278752686181965979242418168549001688583912255923197205586068236163700120096800229812648724185932269320562237853532952389627116550571912841686805658148701709083663215300007997562796838504780938447
,7185420346923218117712852895204393001449718032913337929659165243546699621982252885140314752842932268809290066850494274818658255732553780946841081458928426845109705381938426596705077876429961414922171856816532038967965370606611574541221330124791474283915760838063341024621643218017655843893792619711429488740034405704862248869749889413152481559618619
,1559876147742992673125957404768949712978720573116974723188491435550196169965040848206868200084918233743662847668000971402407461887306389122707315529364807593342507936022301657320206278702095378618110195051280478534126716517153056984269659532882692418682262081495725304483536777013188527470348249542840277926802938912332306310470632601156641005608958891
,21559876147742992673125957404768949712978720573116974723188491435550196169965040848206868200084918233743662847668000971402407461887306389122707315529364807593342507936022301657320206278702095378618110195051280478534126716517153056984269659532882692418682262081495725304483536777013188527470348249542840277926802938912332306310470632601156641005608958891
]
    repetitions = 20

    for number in numbers:

        rst, pr = is_probable_prime(281, repetitions=repetitions, mode='fermat')
        print(f"{281} 有 {pr} 的概率 为 {'素数' if rst else '合数'} ")