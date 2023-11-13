from abc import ABC, abstractmethod
from math import pi


class Figure(ABC):  # https://docs.python.org/3/library/abc.html
    @abstractmethod
    def square(self):
        pass


class Circle(Figure):
    __name__ = "Circle"

    def __init__(self, radius):
        self.radius = radius

    def square(self):
        return pi * self.radius ** 2


class Rectangle(Figure):
    __name__ = "Rectangle"

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def square(self):
        return self.a * self.b


class Triangle(Figure):
    __name__ = "Triangle"

    def __init__(self, base, height):
        self.base = base
        self.height = height

    def square(self):
        return self.base * self.height


if __name__ == '__main__':
    circle1 = Circle(3)
    rectangle1 = Rectangle(1, 2)
    triangle1 = Triangle(3, 4)

    print("Value_circle1_area: ", circle1.square())
    print("Inheritance Tree_circle1: ", circle1.__class__.__mro__)
    print("Value_rectangle1_area: ", rectangle1.square())
    print("Inheritance Tree_rectangle1: ", rectangle1.__class__.__mro__)
    print("Value_triangle1_area: ", triangle1.square())
    print("Inheritance Tree_triangle1: ", triangle1.__class__.__mro__)
