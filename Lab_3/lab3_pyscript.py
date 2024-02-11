#Calculate area of different shapes

import math

class Shape: 
    pass

class Rectangle(Shape):
    def __init__(self, l, w):
        self.l = l
        self.w = w
    def getArea(self):
        return self.l * self.w
    
class Triangle(Shape):
    def __init__(self, b, h):
        self.b = b
        self.h = h
    def getArea(self):
        return 0.5 * self.b * self.h
    
class Circle(Shape):
    def __init__(self,r):
        self.r = r
    def getArea(self):
        return math.pi * self.r * self.r

    
def readData(file):
    shapes = [line.rstrip('\n') for line in file]
    for shape in shapes:
        tokens = shape.split(',')
        if tokens[0] == 'Rectangle':
            shape = Rectangle(int(tokens[1]),int(tokens[2]))
        elif tokens[0] == 'Triangle':
            shape = Triangle(int(tokens[1]),int(tokens[2]))
        elif tokens[0] == 'Circle':
            shape = Circle(int(tokens[1]))
        print("Area of", tokens[0] , "is", shape.getArea())

file = open("Lab_3\shape.txt", "r")
x = readData(file)