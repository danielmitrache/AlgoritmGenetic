import math

class Converter:
    def __init__(self, left: int | float, right: int | float, prec: int | float):
        self.left = left
        self.right = right
        self.prec = prec

        self.n = math.ceil(math.log2((right - left) * (10 ** prec)))
        self.step = (right - left) / (2 ** self.n)


    def __c2b(self, x: int | float) -> str:
        b = []
        while x:
            b.append(x % 2)
            x //= 2
        while len(b) < self.n:
            b.append(0)
        b = "".join(map(str,b[::-1]))
        return b


    def encode(self, num: int | float) -> str:
        idx_interval = int((num - self.left) / self.step)
        idx_interval = min(idx_interval, 2 ** self.n - 1)
        return self.__c2b(idx_interval)


    def decode(self, num: str) -> float:
        idx = int(num, 2)
        value = self.left + idx * self.step
        return value
