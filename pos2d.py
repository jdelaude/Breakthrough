from math import hypot

class Pos2D:
    '''
    Position 2-dimensionnelle (soit (x, y), soit (ligne, colonne)).

    Args:
        row (int): ligne/position verticale
        col (int): colonne/position horizontale

    Attributes:
        x (int): position horizontale
        y (int): position verticale
        row (int): référence vers y
        col (int): référence vers x
    '''
    def __init__(self, row, col):
        self.x_ = col
        self.y_ = row

    @property
    def x(self):
        return self.x_

    @property
    def y(self):
        return self.y_

    @property
    def col(self):
        return self.x_

    @property
    def row(self):
        return self.y_

    def dist_to(self, other, manhattan=False):
        '''
        Calcule la distance L^1 ou L^2 entre ce point et un autre point du plan.

        Args:
            other (Pos2D): point par rapport auquel on calcule la distance
            manhattan (bool): True pour distance L^1 et False pour L^2

        Returns:
            float: distance entre self et other
        '''
        delta = self - other
        return abs(delta.x) + abs(delta.y) if manhattan \
          else hypot(delta.x, delta.y)

    def __eq__(self, other):
        ''' Retourne self == other ''' 
        return isinstance(other, Pos2D) and self.x == other.x and self.y == other.y

    def __sub__(self, other):
        ''' Retourne self - other '''
        if isinstance(other, tuple) and len(other) == 2:
            other = Pos2D(other[1], other[0])
        return Pos2D(
            self.row - other.row,
            self.col - other.col
        )

    def __add__(self, other):
        ''' Retourne self + other '''
        if isinstance(other, tuple) and len(other) == 2:
            other = Pos2D(other[1], other[0])
        return Pos2D(
            self.row + other.row,
            self.col + other.col
        )

    def __lt__(self, other):
        ''' Return self < other '''
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __str__(self):
        return f'({self.x_}, {self.y_})'

    # Nécessaire pour mettre des Pos2D dans un dict ou un set
    # c.f. VALID_MOVES
    def __hash__(self):  
        return hash(str(self))

