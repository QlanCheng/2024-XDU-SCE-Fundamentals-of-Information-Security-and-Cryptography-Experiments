class EllipticCurve:
    def __init__(self):
        """
        y^2 = x^3 + ax + b (mod p)
        """
        self.p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
        self.a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
        self.b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
        self.n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123  # 阶

    def __eq__(self, other):
        """重载等于运算符"""
        return self.p == other.p and self.a == other.a and self.b == other.b and self.n == other.n

class EllipticCurvePoint(EllipticCurve):
    def __init__(self, x, y):
        super().__init__()
        self.infinity = (x is None) and (y is None)  # 无穷远点
        if not self.infinity:
            self.x = x
            self.y = y
            if not self.validate():
                raise ValueError('点不在椭圆曲线上')

    def __eq__(self, other):
        """重载等于运算符，比较两个点是否相等"""
        # 比较点坐标 和 曲线参数是否一样
        return (self.x == other.x and self.y == other.y
                and self.p == other.p and self.a == other.a and self.b == other.b and self.n == other.n)

    def __neg__(self):
        """
        重载取反运算
        """
        if self.infinity:
            return self  # 无穷远点的负值仍是无穷远点
        return EllipticCurvePoint(self.x, -self.y % self.p)

    def __add__(self, other):
        """重载加法运算"""
        if self.infinity:
            return other
        if other.infinity:
            return self

        # 如果加上相反点，则返回无穷远点
        if other == -self:
            return EllipticCurvePoint(None, None)

        # 计算斜率
        if self == other:  # 如果是相同点
            k = ((3 * self.x ** 2 + self.a) * pow(2 * self.y, -1, self.p)) % self.p
        else:  # 如果是不同点
            k = ((other.y - self.y) * pow(other.x - self.x, -1, self.p)) % self.p

        x3 = (k ** 2 - self.x - other.x) % self.p
        y3 = (k * (self.x - x3) - self.y) % self.p
        return EllipticCurvePoint(x3, y3)

    def __mul__(self, scalar):
        """椭圆曲线点标量乘法（倍点计算，使用双倍加算法）"""
        if not isinstance(scalar, int):
            raise TypeError("Scalar multiplication only supports integers.")
        if scalar < 0:
            return -self * -scalar

        result = EllipticCurvePoint(None, None)  # 无穷远点
        addend = self

        while scalar:
            if scalar & 1:
                result += addend
            addend += addend
            scalar >>= 1

        return result

    def __rmul__(self, scalar):
        """标量左乘：scalar * point"""
        return self.__mul__(scalar)

    def __str__(self):
        if self.infinity:
            return "Infinity 无穷远点"

        string = f"""点坐标 ({self.x}, {self.y})\n椭圆曲线参数 (y^2 = x^3 + {self.a} * x + {self.b})"""
        return string

    def validate(self):
        """确认自己是不是椭圆曲线上的点"""
        return pow(self.y, 2, self.p) == (self.x ** 3 + self.a * self.x + self.b) % self.p

    def to_bytes(self):
        """因为 x, y坐标最多都是32字节长
        所以固定表示成 64 字节的bytes, 前32位指示x, 后32位指示y"""
        x_bytes = self.x.to_bytes(32, byteorder='big')
        y_bytes = self.y.to_bytes(32, byteorder='big')
        return x_bytes + y_bytes

    @staticmethod
    def from_bytes(data: bytes):
        """
        从64字节的bytes读取x, y，并初始化一个椭圆曲线点。
        前32字节为x坐标，后32字节为y坐标。
        """
        if len(data) != 64:
            raise ValueError("不是64位长的")

        # 分别解析 x 和 y 坐标
        x = int.from_bytes(data[:32], byteorder='big')
        y = int.from_bytes(data[32:], byteorder='big')

        # 初始化一个椭圆曲线点
        point = EllipticCurvePoint(x, y)
        point.validate()
        return point

G_x = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
G_y = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G = EllipticCurvePoint(G_x, G_y)

if __name__ == '__main__':
    G_x = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    G_y = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    point1 = EllipticCurvePoint(G_x, G_y)
    b = point1.to_bytes()
    point2 = EllipticCurvePoint.from_bytes(b)
    print(point1 == point2)

