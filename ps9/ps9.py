# 6.00 Problem Set 9
#
# Name:
# Collaborators:
# Time:

from string import *

class Shape(object):
    def area(self):
        raise AttributeException("Subclasses should override this method.")

class Square(Shape):
    def __init__(self, h):
        """
        h: length of side of the square
        """
        self.side = float(h)
    def area(self):
        """
        Returns area of the square
        """
        return self.side**2
    def __str__(self):
        return 'Square with side ' + str(self.side)
    def __eq__(self, other):
        """
        Two squares are equal if they have the same dimension.
        other: object to check for equality
        """
        return type(other) == Square and self.side == other.side

class Circle(Shape):
    def __init__(self, radius):
        """
        radius: radius of the circle
        """
        self.radius = float(radius)
    def area(self):
        """
        Returns approximate area of the circle
        """
        return 3.14159*(self.radius**2)
    def __str__(self):
        return 'Circle with radius ' + str(self.radius)
    def __eq__(self, other):
        """
        Two circles are equal if they have the same radius.
        other: object to check for equality
        """
        return type(other) == Circle and self.radius == other.radius

#
# Problem 1: Create the Triangle class
#
## TO DO: Implement the `Triangle` class, which also extends `Shape`.

class Triangle(Shape):
    def __init__(self, base, height):
        """
        base: base of a triangle
        height: height of a triangle
        """
        self.base = float(base)
        self.height = float(height)
    def area(self):
        """
        Returns area of triangle
        """
        return 0.5*self.base*self.height
    def __str__(self):
        return "Triangle with base " + str(self.base) + " and height " + str(self.height)
    def __eq__(self, other):
        """
        Two triangles are equal if they have the same base and height.
        other: object to check for equality
        """
        return type(other) == Triangle and self.base == other.base and self.height == other.height
    
#
# Problem 2: Create the ShapeSet class
#
## TO DO: Fill in the following code skeleton according to the
##    specifications.

class ShapeSet:
    shapeList = []
    def __init__(self):
        """
        Initialize any needed variables
        """
        ## TO DO
    def addShape(self, sh):
        """
        Add shape sh to the set; no two shapes in the set may be
        identical
        sh: shape to be added
        """
        ## TO DO
        self.shapeList.append(sh)
    def __iter__(self):
        """
        Return an iterator that allows you to iterate over the set of
        shapes, one shape at a time
        """
        ## TO DO
        for i in self.shapeList:
            yield i
    def __str__(self):
        """
        Return the string representation for a set, which consists of
        the string representation of each shape, categorized by type
        (circles, then squares, then triangles)
        """
        ## TO DO
        s = ""
        for i in range(len(self.shapeList)):
            s = s + str(self.shapeList[i]) + "\n"
        return s
##triangle1 = Triangle(2, 3)
##circle1 = Circle(3)
##shapes = ShapeSet()
##shapes.addShape(triangle1)
##shapes.addShape(circle1)
##print str(shapes)
##for i in shapes:
##    print i
        
#
# Problem 3: Find the largest shapes in a ShapeSet
#
##
##triangle1 = Triangle(2, 3)
##triangle2 = Triangle(4, 5)
##circle1 = Circle(2)
##square1 = Square(4)
##square2 = Square(2)
##diffshapes = ShapeSet()
##diffshapes.addShape(triangle1)
##diffshapes.addShape(triangle2)
##diffshapes.addShape(circle1)
##diffshapes.addShape(square1)
##diffshapes.addShape(square2)
##print diffshapes
def findLargest(shapes):
    """
    Returns a tuple containing the elements of ShapeSet with the
       largest area.
    shapes: ShapeSet
    """
    ## TO DO
    maximum = 0
    for shape in shapes:
        if shape.area() > maximum:
            maximum = shape.area()
            max_shape = shape
    return (str(max_shape), maximum)
#
# Problem 4: Read shapes from a file into a ShapeSet
#
def readShapesFromFile(filename):
    """
    Retrieves shape information from the given file.
    Creates and returns a ShapeSet with the shapes found.
    filename: string
    """
    ## TO DO
    shapeset = ShapeSet()
    shapes = []
    shapes_list = open(filename, "r", 0)
    for line in shapes_list:
        s = ""
        check = False
        for i in range(len(line)-1):
            if line[i] == "(" or check == True:
                s = s + line[i+1]
                check = True
        s = s[0:-2]
        if "Square" in line:
            print s
            param = float(s)
            shapeset.addShape(Square(param))
            print shapeset
        if "Circle" in line:
            print s
            param = float(s)
            shapeset.addShape(Circle(param))
            print shapeset
        if "Triangle" in line:
            print s
            param1 = float(s[0])
            param2 = float(s[2])
            shapeset.addShape(Triangle(param1, param2))
            print shapeset
    print shapeset

readShapesFromFile("shapes.txt")
