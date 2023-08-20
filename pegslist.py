from pos2d import Pos2D

class PegsList:
    '''
    Liste des pions d'un joueur.
    '''
    def __init__(self):
        self.positions_ = []

    def add(self, pos):
        '''
        Ajoute un pion au conteneur.

        Args:
            pos (Pos2D): position du pion à ajouter
        '''
        self.positions_.append(pos)

    def remove(self, pos):
        '''
        Retire un pion du conteneur.

        Args:
            pos (Pos2D): position du pion à retirer
        '''
        self.positions_.remove(pos)

    def move(self, move):
        '''
        Modifie la position d'un pion par un déplacement.

        Args:
            move (Move): déplacement du joueur
        '''
        idx = self.positions_.index(move.src)
        self.positions_[idx] = move.dest

    def has_intersection_with(self, other):
        '''
        Détermine si une position occupée par le joueur est également dans un
        autre conteneur.

        Args:
            other (Iterator[Pos2D]): autre conteneur

        Returns:
            bool: True s'il y a au moins une position en commun et False sinon
        '''
        return len(set(self) & set(other)) > 0

    def __iter__(self):
        return iter(self.positions_)

    def __len__(self):
        return len(self.positions_)

