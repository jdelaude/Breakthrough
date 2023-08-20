from pos2d import Pos2D

class Move:
    '''
    Déplacement d'un pion sur le plateau.

    Attributes:
        src (Pos2D): position de départ du pion déplacé
        dest (Pos2D): position d'arrivée du pion déplacé
        player (int): PLAYER1 ou PLAYER2
        elta (Pos2D): vecteur de déplacement depuis src vers dest
    '''
    def __init__(self, src, dest, player):
        self.src_ = src
        self.dest_ = dest
        self.player_ = player

    @property
    def src(self):
        return self.src_

    @property
    def dest(self):
        return self.dest_

    @property
    def player(self):
        return self.player_

    @property
    def delta(self):
        return self.dest_ - self.src_

    def __reversed__(self):
        '''
        Renvoie le mouvement inverse du mouvement représenté.

        Returns:
            Move: mouvement depuis dest vers src
        '''
        return Move(self.dest_, self.src_, self.player_)

    def __str__(self):
        return f'<{self.player_} moves from {self.src_} to {self.dest_}>'
