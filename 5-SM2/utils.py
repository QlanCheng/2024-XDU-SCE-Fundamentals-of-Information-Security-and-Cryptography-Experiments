def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    if len(b1) != len(b2):
        raise ValueError("字节长度必须一样")

    # 将每个字节按位异或并返回结果
    return bytes([byte1 ^ byte2 for byte1, byte2 in zip(b1, b2)])


def split_bytes(data: bytes) -> tuple:
    """
    将一个bytes对象分成三段：前64字节，中间部分，后32字节。
    """
    if len(data) < 96:
        raise ValueError("Input data must be at least 64 bytes long.")

    front = data[:64]  # 前64字节
    back = data[-32:]  # 后32字节
    middle = data[64:-32]  # 中间部分

    return front, middle, back

if __name__ == '__main__':
    x = 2
    y = 0
    p = 7
    print((y**2 % p) == (x**3 + x**2 + 2) % p)