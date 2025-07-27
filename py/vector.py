import includes     # for global vars
from includes import *


class Vector(object):
    """
        Vector of any dimension greater or equal to 2.
        Modified class from Mat Leonard's on Github: https://gist.github.com/mcleonard/5351452
    """
    def __init__(self, *args):
        """ Create a vector, example: v = Vector(1,2) """
        if len(args)==0: self.values = [0, 0]
        elif len(args)==1: self.values = [args[0], 0]
        else: self.values = list(args)
    
    @staticmethod
    def random(min : float, max : float, dimensions = None) -> 'Vector':
        if dimensions is None:
            assert(max > 0), "Max must be strictly positive for random vector dimension."
            dimensions = round(random_number(0, max))
        return Vector(*[random_number(min, max) for _ in range(dimensions)])
    
    @staticmethod
    def zero(dimensions : int) -> 'Vector':
        return Vector(*[0 for _ in range(dimensions)])
    
    @staticmethod
    def create_random_pos_in_window() -> 'Vector':
        return Vector(random_number(0, WIN_WIDTH), random_number(0, WIN_HEIGHT))
    
    # Shorthands for 2D and 3D
    @property
    def x(self):
        # self.values is guaranteed to contain at least 2 elements since self.dimension >= 2 is always true
        return self.values[0]
    @property
    def y(self):
        return self.values[1]
    @property
    def z(self):
        assert(self.dimension >= 3), "Vector too small for y."
        return self.values[2]
    
    @property
    def tuple_2D(self) -> tuple[int, int]:
        return (self.values[0], self.values[1])
    @property
    def tuple_3D(self) -> tuple[int, int, int]:
        assert(self.dimension >= 3), "Expected 3D vector or higher dimension"
        return (self.values[0], self.values[1], self.values[1])
    
    @property
    def dimension(self) -> int:
        return len(self.values)
    
    @x.setter
    def x(self, val):
        self.values[0] = val
    @y.setter
    def y(self, val):
        self.values[1] = val
    @z.setter
    def z(self, val):
        if self.dimension == 2:
            self.values.append(0)
        self.values[2] = val
    
    def norm(self):
        """ Returns the norm (length, magnitude) of the vector """
        return math.sqrt(sum( x*x for x in self ))
        
    def argument(self, radians=False):
        """ Returns the argument of the vector, the angle clockwise from +y. In degress by default, 
            set radians=True to get the result in radians. This only works for 2D vectors. """
        arg_in_rad = math.acos(self.y / self.norm())
        if radians:
            return arg_in_rad
        arg_in_deg = math.degrees(arg_in_rad)
        
        if self.values[0] < 0: 
            return 360 - arg_in_deg
        return arg_in_deg
    
    def normalize(self):
        """ Returns a normalized unit vector """
        norm = self.norm()
        normed = tuple( x / norm for x in self )
        return self.__class__(*normed)
    
    def rotate(self, theta):
        """ Rotate this vector. If passed a number, assumes this is a 
            2D vector and rotates by the passed value in degrees.  Otherwise,
            assumes the passed value is a list acting as a matrix which rotates the vector.
        """
        if isinstance(theta, (int, float)):
            # So, if rotate is passed an int or a float...
            if self.dimension != 2:
                raise ValueError("Rotation axis not defined for greater than 2D vector")
            return self._rotate2D(theta)
        
        matrix = theta
        if not all(len(row) == len(self) for row in matrix) or not len(matrix)==len(self):
            raise ValueError("Rotation matrix must be square and same dimensions as vector")
        return self.matrix_mult(matrix)
        
    def _rotate2D(self, theta):
        """ Rotate this vector by theta in degrees.
            
            Returns a new vector.
        """
        theta = math.radians(theta)
        # Just applying the 2D rotation matrix
        dc, ds = math.cos(theta), math.sin(theta)
        x, y = self.values
        x, y = dc*x - ds*y, ds*x + dc*y
        return self.__class__(x, y)
        
    def matrix_mult(self, matrix):
        """ Multiply this vector by a matrix.  Assuming matrix is a list of lists.
        
            Example:
            mat = [[1,2,3],[-1,0,1],[3,4,5]]
            Vector(1,2,3).matrix_mult(mat) ->  (14, 2, 26)
         
        """
        if not all(len(row) == len(self) for row in matrix):
            raise ValueError('Matrix must match vector dimensions') 
        
        # Grab a row from the matrix, make it a Vector, take the dot product, 
        # and store it as the first component
        product = tuple(Vector(*row)*self for row in matrix)
        
        return self.__class__(*product)
    
    def dot(self, vector):
        """ Returns the dot product (inner product) of self and another vector
        """
        if not isinstance(vector, Vector):
            raise ValueError('The dot product requires another vector')
        return sum(a * b for a, b in zip(self, vector))
    
    def __mul__(self, other):
        """ Returns the dot product of self and other if multiplied
            by another Vector.  If multiplied by an int or float,
            multiplies each component by other.
        """
        if isinstance(other, Vector):
            return self.dot(other)
        elif isinstance(other, (int, float)):
            product = tuple( a * other for a in self )
            return self.__class__(*product)
        else:
            raise ValueError("Multiplication with type {} not supported".format(type(other)))
    
    def __rmul__(self, other):
        """ Called if 4 * self for instance """
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, Vector):
            divided = tuple(self[i] / other[i] for i in range(self.dimension))
        elif isinstance(other, (int, float)):
            divided = tuple( a / other for a in self )
        else:
            raise ValueError("Division with type {} not supported".format(type(other)))
        
        return self.__class__(*divided)
    
    def __add__(self, other):
        """ Returns the vector addition of self and other """
        if isinstance(other, Vector):
            added = tuple( a + b for a, b in zip(self, other) )
        elif isinstance(other, (int, float)):
            added = tuple( a + other for a in self )
        else:
            raise ValueError("Addition with type {} not supported".format(type(other)))
        
        return self.__class__(*added)
    
    def __radd__(self, other):
        """ Called if 4 + self for instance """
        return self.__add__(other)
    
    def __sub__(self, other):
        """ Returns the vector difference of self and other """
        if isinstance(other, Vector):
            subbed = tuple( a - b for a, b in zip(self, other) )
        elif isinstance(other, (int, float)):
            subbed = tuple( a - other for a in self )
        else:
            raise ValueError("Subtraction with type {} not supported".format(type(other)))
        
        return self.__class__(*subbed)
    
    def __pos__(self):
        return self
    def __neg__(self):
        return Vector.zero(self.dimension) - self
    
    def __rsub__(self, other):
        """ Called if 4 - self for instance """
        return self.__sub__(other)
    
    def __iter__(self):
        return self.values.__iter__()
    
    def __len__(self):
        return len(self.values)
    
    def __getitem__(self, key):
        return self.values[key]
        
    def __repr__(self):
        return str(self.values)