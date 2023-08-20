from const import *
from errors import *
from matrix import Matrix
from move import *
from pegslist import PegsList
from pos2d import Pos2D

class HistoryEntry:
    '''
    Entrée de l'historique des coups joués sur le plateau.

    Attributes:
        move (Move): déplacement du pion
        captured (bool): True si un pion adverse a été capturé par ce déplacement
    '''

    def __init__(self, move, captured=False):
        self.move_ = move
        self.captured_ = captured

    @property
    def move(self):
        return self.move_

    @property
    def captured(self):
        return self.captured_

class Board:
    '''
    Plateau de jeu.

    Args:
        rows (int): nombre de lignes du plateau
        cols (int): nombre de colonnes du plateau

    Attributes:
        matrix (Matrix): représentation matricielle du plateau de jeu
        pegs (List[PegsList]): liste des pions blancs et noirs
        history (List[HistoryEntry]): historique des coups joués sur le plateau
        last_move (HistoryEntry): dernier coup présent dans l'historique
        m (int): nombre de lignes du plateau
        n (int): nombre de colonnes du plateau
        nb_pegs (int): nombre de pions restant sur le plateau, tous joueurs confondus
        winner (int): PLAYER1 si le joueur 1 a gagné la partie,
                      PLAYER2 si le joueur 2 a gagné
                      et None si la partie n'est pas finie
        .
    '''
    def __init__(self, rows, cols):
        self.matrix_ = Matrix(rows, cols, EMPTY)
        self.white_pegs_ = PegsList()
        self.black_pegs_ = PegsList()
        self.pegs_ = [
            self.white_pegs_,
            self.black_pegs_
        ]
        self.history_ = []

    @property
    def m(self):
        return self.matrix_.m

    @property
    def n(self):
        return self.matrix_.n

    @property
    def nb_pegs(self):
        return sum(map(len, self.pegs_))

    @property
    def pegs(self):
        return self.pegs_


    def add_white_peg(self, pos):
        '''
        Ajoute un pion au joueur blanc à la position donnée.

        Args:
            pos (Pos2D): position à laquelle ajouter le pion
        '''
        self.__add_peg(pos, PLAYER1)

    def add_black_peg(self, pos):
        '''
        Ajoute un pion au joueur noir à la position donnée.

        Args:
            pos (Pos2D): position à laquelle ajouter le pion
        '''
        self.__add_peg(pos, PLAYER2)

    def __add_peg(self, pos, player):
        '''
        Ajoute un pion au joueur donné à la position donnée.

        Args:
            pos (Pos2D): position à laquelle ajouter le pion
            player (int): joueur auquel ajouter le pion

        Raises:
            InvalidPositionError: s'il est impossible d'ajouter le pion
        '''
        if self.matrix_[pos] != EMPTY:
            raise InvalidPositionError(
                f'Case {pos} déjà occupée par: {self.matrix_[pos]}'
            )
        self.matrix_[pos] = player
        self.pegs_[player-1].add(pos)

    def check_integrity(self):
        '''
        Vérifie si le plateau représenté est valide, i.e.
        (i)  aucune case n'est occupée par deux joueurs simultanément
        (ii) la matrice du plateau et les listes de positions représentent le même plateau

        Returns:
            bool: True si le plateau est ok et False sinon
        '''
        if self.white_pegs_.has_intersection_with(self.black_pegs_):
            return False
        for pos in self.white_pegs_:
            if self.matrix_[pos] != PLAYER1:
                return False
        for pos in self.black_pegs_:
            if self.matrix_[pos] != PLAYER2:
                return False
        nb_empty = self.matrix_.size - self.nb_pegs
        if self.matrix_.count(EMPTY) != nb_empty:
            return False
        return True

    def print(self, special_position=None, special_char='#'):
        '''
        Affiche le plateau de jeu avec possibilité de mettre une case en évidence.

        Args:
            special_position (Pos2D): position à mettre en évidence (None si aucune)
            special_char (str): caractère de mise en évidence
        '''
        m = self.matrix_.m
        n = self.matrix_.n
        for i in range(m):
            print(m - i, end=' ')  # indices croissant de bas en haut
            for j in range(n):
                pos = Pos2D(i, j)
                end = ' ' if j < n - 1 else '\n'
                print(
                    special_char if pos  == special_position \
                                 else CHARS[self.matrix_[pos]],
                    end=end
                )
        print(' ', ' '.join(ALPHABET[:n]))

    @property
    def last_move(self):
        return self.history_[-1].move if self.history_ else None

    def possible_moves_from_source(self, src, player):
        '''
        Génère tous les mouvements possibles pour un pion donné d'un joueur donné.

        Args:
            src (Pos2D): position de départ
            player (int): PLAYER1 ou PLAYER2

        Returns:
            Iterator[Move]:
                générateur des mouvements valides d'un pion de `player`
                placé en position `src`
        '''
        for delta in VALID_MOVES[player-1]:
            dest = src + delta
            move = Move(src, dest, player)
            if self.matrix_.is_valid_pos(dest) and self.is_valid_direction(move):
                yield move

    def _possible_moves(self, player):
        '''
        Génère tous les mouvements possibles que peut faire un joueur.

        Args:
            player (int): PLAYER1 ou PLAYER2

        Returns:
            Iterator[Move]: générateur des mouvemens valides de `player`
        '''
        for src in self.pegs_[player-1]:
            yield from self.possible_moves_from_source(src, player)

    def possible_moves(self, player):
        '''
        Génère tous les mouvements possibles que peut faire un joueur.
        Cette méthode-ci génère tous les coups possibles et puis les renvoie dans un
        conteneur, contrairement à _possible_moves qui les génère au fur et à mesure
        qu'ils sont demandés.

        Args:
            player (int): PLAYER1 ou PLAYER2

        Returns:
            List[Move]: liste des mouvements valides de `player`.
        '''
        return list(self._possible_moves(player))

    def is_valid_direction(self, move):
        '''
        Détermine si un mouvement est valide.

        Args:
            move (Move): mouvement à tester.

        Returns:
            bool:
                True si le déplacement est valide pour le joueur en question
                et False sinon
        '''
        delta = move.delta
        player = move.player
        return delta in VALID_MOVES[player-1] and \
               ((delta.x == 0 and self.matrix_[move.dest] == EMPTY) \
             or (delta.x != 0 and self.matrix_[move.dest] != player))

    def can_move_from(self, pos):
        '''
        Détermine s'il y a un pion pouvant se déplacer en position donnée.

        Args:
            pos (Pos2D): position à vérifier

        Returns:
            bool: True s'il y a un pion ayant au moins un mouvement valide et False sinon
        '''
        player = self.matrix_[pos]
        if player == EMPTY:
            return False
        # on passe ici par un générateur car il n'est pas nécessaire d'engendrer la liste
        # de tous les mouvements valides depuis pos pour savoir s'il y en a au moins un.
        generator = self.possible_moves_from_source(pos, player)
        try:
            next(generator)
        except StopIteration:
            return False
        else:
            return True

    @property
    def winner(self):
        # Pas besoin de vérifier l'entièreté de la première et de la dernière ligne
        # puisque la partie n'est finie que si le dernier coup est un coup final.
        # Au lieu de faire 2n comparaisons, on peut vérifier si la partie est
        # terminée en O(1), et ça c'est beau.
        last_move = self.last_move
        if last_move is None:
            return None
        last_player = last_move.player
        last_y = last_move.dest.y
        return PLAYER1 if last_y == 0 and last_player == PLAYER1 \
          else PLAYER2 if last_y == self.m-1 and last_player == PLAYER2 \
          else PLAYER1 if len(self.pegs_[0]) == 0 \
          else PLAYER2 if len(self.pegs_[1]) == 0 \
          else None

    def move(self, move):
        '''
        Effectue le coup demandé sur le plateau.

        Args:
            move (Move): action à effectuer
        '''
        player = move.player
        other_player = 3-player
        entry = HistoryEntry(move, self.matrix_[move.dest] == other_player)
        if entry.captured:
            # pas besoin de gérer le cas où move.dest n'existe pas dans
            # self.pegs_[2-player] puisque par construction nous savons que tout objet
            # de type Player (ou spécialisation) renvoie un coup valide
            self.pegs_[2-player].remove(move.dest)
        self.matrix_[move.src] = EMPTY
        self.matrix_[move.dest] = player
        self.pegs_[player-1].move(move)
        self.history_.append(entry)

    def undo(self):
        '''
        Annule le dernier coup qui a été joué sur le plateau.

        Raises:
            EmptyHistoryError: si l'historique est vide
        '''
        try:
            last_entry = self.history_.pop()
        except IndexError:
            raise EmptyHistoryError('Aucun coup à annuler')
        last_move = last_entry.move
        other_player = 3-last_move.player
        self.matrix_[last_move.src] = last_move.player
        self.pegs_[last_move.player-1].move(reversed(last_move))
        # si la dernière action a capturé un pion adversaire,
        # il faut penser à le restituer
        if last_entry.captured:
            self.matrix_[last_move.dest] = other_player
            self.pegs_[other_player-1].add(last_move.dest)
        else:
            self.matrix_[last_move.dest] = EMPTY

