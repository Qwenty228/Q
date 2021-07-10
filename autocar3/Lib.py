from math import atan2, pi
import numpy as np

class Vector:
    pass


class Vector:

    def __init__(self, dimension=[0, 0]):
        if type(dimension) == Vector:
            self.x, self.y = dimension.x, dimension.y
        else:
            self.x, self.y = dimension
        

    def __add__(self, other: Vector) -> Vector:
        return Vector([self.x + other.x, self.y + other.y])

    def __sub__(self, other: Vector) -> Vector:
        return self.__add__(other.__mul__(-1))

    def __mul__(self, other):
        return Vector([self.x * other, self.y * other])

    def size(self) -> float:
        return (self.x**2 + self.y**2)**(0.5)

    def ang(self):
        return atan2(self.y, self.x)

    def dist(self, other: Vector) -> Vector:
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5


def map_range(current, OldMin, OldMax, NewMin, NewMax):
    return ((current - OldMin) / (OldMax - OldMin) ) * (NewMax - NewMin) + NewMin

    
def fromCharCode(args):
    if type(args) == int:
        args = [args]
    return ''.join(map(chr, args))


