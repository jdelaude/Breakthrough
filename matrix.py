from pos2d import Pos2D

class Matrix:
    '''
    Matrice numérique de taille m x n.

    Args:
        m (int): nombre de lignes
        n (int): nombre de colonnes
        init (int/float): valeur par défaut des entrées de la matrice

    Attributes:
        m (int): nombre de lignes
        n (int): nombre de colonnes
        shape (tuple): (m, n)
        size (int): nombre d'éléments dans la matrice
    '''
    def __init__(self, m, n, init=0.):
        self.m_ = m
        self.n_ = n
        self.buffer_ = [
            [init for x in range(n)] \
            for y in range(m)
        ]

    @property
    def m(self):
        return self.m_

    @property
    def n(self):
        return self.n_

    @property
    def shape(self):
        return (self.m, self.n)

    @property
    def size(self):
        return self.m * self.n

    def is_valid_pos(self, pos):
        '''
        Vérifie si une position donnée correspond à un indiçage valide de la matrice.

        Args:
            pos (Pos2D): position d'indiçage

        Returns:
            bool: True si l'inddiçage ests valide et False sinon
        '''
        return 0 <= pos.row < self.m \
           and 0 <= pos.col < self.n

    def __check_pos(self, pos):
        '''
        Formatte la position d'indiçage correctement et vérifie si elle est valide.

        Args:
            pos (tuple/Pos2D): indiçage de la matrice.

        Returns:
            Pos2D: pos converti en Pos2D si nécessaire

        Raises:
            IndexError: si pos n'est pas une position valide
        '''
        if isinstance(pos, tuple) and len(pos) == 2:
            x, y = pos
            pos = Pos2D(y, x)
        assert isinstance(pos, Pos2D)
        if not self.is_valid_pos(pos):
            raise IndexError(
                f'Position invalide dans une matrice de taille {self.shape}: {pos}'
            )
        return pos

    def __getitem__(self, pos):
        '''
        Récupère l'élément à une position (i, j) donnée.

        Args:
            pos (Pos2D/tuple): indiçage de la matrice.

        Returns:
            int/float: valeur à l'entrée pos

        Raises:
            IndexError: si pos n'est pas une position valide
        '''
        pos = self.__check_pos(pos)
        return self.buffer_[pos.y][pos.x]

    def __setitem__(self, pos, value):
        '''
        Remplace l'élément à une position (i, j) donnée.

        Args:
            pos (Pos2D/tuple): indiçage de la matrice
            value (int/float): nouvelle valeur

        Raises:
            IndexError: si pos n'est as une position valide
        '''
        pos = self.__check_pos(pos)
        self.buffer_[pos.y][pos.x] = value

    def count(self, value):
        '''
        Comte le nombre d'occurrences d'une valeur donnée dans la matrice.

        Args:
            value (int/float): valeur à compter dans la matrice.

        Returns:
            int: nombre d'occurrences de `value` dans la matrice.
        '''
        return sum(row.count(value) for row in self.buffer_)
