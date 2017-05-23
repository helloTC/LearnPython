from math import hypot

class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector(%r, %r)" % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x,y)

    def __bool__(self):
        return bool(abs(self))

    def __mul__(self, scalar):
        return Vector(self.x*scalar, self.y*scalar)

if __name__ == "__main__":
    v1 = Vector(3,4)
    v2 = Vector(2,2)

    print('Addition...')
    print(v1+v2)

    print('Multiple...')
    print((v1*5))

    print('Distance...')
    print('Length of v1 is {}'.format(abs(v1)))

