import math

class Vec2:
    def __init__(self, pos=(0,0)):
        self.x, self.y = pos
        self.position = pos
        self.mag = self.get_mag()

    def get_mag(self):
        len = math.sqrt(self.x**2 + self.y**2)
        if len == 0:
            return 0.1
        return len
    
    def normalise(self):
        return Vec2((self.x / self.mag, self.y / self.mag))
    
    def update(self,x,y):
        self.x = x
        self.y = y
        self.position = (x,y)
        self.mag = self.get_mag()

    def __add__(self, other):
        return Vec2((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Vec2((self.x - other.x, self.y - other.y))
    
    def __mul__(self, other):
        return Vec2((self.x * other, self.y * other))
    
    def __neg__(self):
        return Vec2((-self.x, -self.y))
    
    def __round__(self, n=0):
        return Vec2((round(self.x,n), round(self.y, n)))

    def __rmul__(self, other):
        # 숫자 * 벡터 (교환 법칙)
        return self.__mul__(other)

    def __truediv__(self, other):
        # 벡터 / 스칼라
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Division by zero.")
            return Vec2((self.x / other, self.y / other))
        else:
            raise ValueError("Vec2 can only be divided by a scalar (int or float).")

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"
