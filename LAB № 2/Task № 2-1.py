import math


class MyVector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, obj):     # +
        return MyVector2D(self.x + obj.x, self.y + obj.y)

    def  __sub__(self, obj):    # -
        return MyVector2D(self.x - obj.x, self.y - obj.y)

    def __iter__(self):     # next(iter(obj : Vector2D))
        yield self.x
        yield self.y

    def __eq__(self, obj):  # ==
        # return True if ((self.x == obj.x) & (self.y == obj.y)) else False
        return self.y == obj.y and self.x == obj.x
        # return True and ((self.x == obj.x) & (self.y == obj.y)) or False (before python v2.7)
        # return (False, True)[(self.x == obj.x) & (self.y == obj.y)]

    def __ne__(self, obj):  # !=
        return not self.__eq__(obj)
        # return True if ((self.x != obj.x) | (self.y != obj.y)) else False
        # return True and ((self.x != obj.x) | (self.y != obj.y)) or False (before python v2.7)
        # return (False, True)[(self.x != obj.x) | (self.y != obj.y)]

    def __mul__(self, obj): # *
        return MyVector2D(self.x * obj.x, self.y * obj.y) if type(obj) is MyVector2D else MyVector2D(self.x * obj, self.y * obj)

    def __len__(self): # TypeError: 'float' object cannot be interpreted as an integer
        return 2    # dimension: Vector_2_D!

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def len(self):  # or 2
        return self.__abs__()

    def __str__(self):
        return "<" + str(self.x) + ";" + str(self.y) + ">"  # Variant № 1
        # return '<{:g} : {:g}>'.format(self.x, self.y) # Variant № 2

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    v2d_1 = MyVector2D(1, 2)
    v2d_2 = MyVector2D(1, 2) * 2
    v2d_3 = v2d_1 + v2d_2
    # v2d_4 = 2 * Vector2D(1, 2) # Error Base Type.
    
    L_v2d_1_1 = len(v2d_1)
    L_v2d_1_2 = v2d_1.len()
    L_v2d_1_3 = v2d_1.__abs__()

    # print(dir(v2d_2))
    print("Vector2.x: ", v2d_2.x, "Vector2.y: ", v2d_2.y)
    iter_v2d_2 = iter(v2d_2)
    print("Vector2.x: ", next(iter_v2d_2), "Vector2.y: ", next(iter_v2d_2))
    # print(v2d_4.x, v2d_4.y)
    print("Vector3.x: ", v2d_3.x, "Vector3.y: ", v2d_3.y)
    print("Variant One len vector1: ",  L_v2d_1_1)
    print("Variant Two len vector1: ",  L_v2d_1_2)
    print("Variant Three len vector1: ", L_v2d_1_3)
    print("Result method __repr__:",    v2d_1)
    
