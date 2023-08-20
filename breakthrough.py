from board import Board
from const import *
from players import *
from pos2d import Pos2D


class Breakthrough:
    def __init__(self, path=None, player2_is_ai=False):
        '''
        Attributes:
            board (Board): le plateau de jeu
            players (List[Player]): liste contenant les deux joueurs.
            winner (int): alias de board.winner
        '''
        self.__init_from_file(path)
        player2_type = MinimaxAiPlayer or MonteCarlo if player2_is_ai == '-ai' else HumanPlayer
        player1 = HumanPlayer(PLAYER1, self.board_)
        player2 = player2_type(PLAYER2, self.board_)
        self.players_ = [
            player1,
            player2
        ]

    def __init_from_file(self, path):
        '''
        Construit le plateau de jeu.

        Args:
            path (str): chemin vers le plateau de jeu
        '''
        if path is None:
            self.__make_default_board()
        else:
            self.__make_board_from_file(path)

    def __make_board_from_file(self, path):
        '''
        Construit le plateau de jeu depuis un fichier.

        Args:
            path (str): chemin vers le plateau de jeu

        Raises:
            BadFormatError: si le fichier fourni est incorrect
        '''
        with open(path, 'r') as f:
            rows, cols = map(int, f.readline().strip().split(' '))
            self.board_ = Board(rows, cols)
            for position in self.__find_positions_from_line(f.readline().strip()):
                self.board_.add_white_peg(position)
            for position in self.__find_positions_from_line(f.readline().strip()):
                self.board_.add_black_peg(position)
        if not self.board_.check_integrity():
            raise BadFormatError(f'Erreur dans le format du fichier "{path}"')

    def __find_positions_from_line(self, line):
        '''
        Lit toutes coordonnées stockées dans une ligne du fichier.

        Args:
            line (str): ligne au format <col><row>(,<col><row>)*

        Returns:
            Iterator[Pos2D]: générateur de positions.
        '''
        row = lambda pos: self.board_.m - int(pos[1:])
        col = lambda pos: ord(pos[0]) - ord('a')
        return (
            Pos2D(row(pos), col(pos)) \
            for pos in line.split(',')
        )

    def __make_default_board(self):
        '''
        Construit un plateau carré n x n par défaut où chaque joueur a 2n pions répartis
        sur 2 lignes (n = DEFAULT_SIZE).
        '''
        self.board_ = Board(DEFAULT_SIZE, DEFAULT_SIZE)
        for i in range(2):
            for j in range(DEFAULT_SIZE):
                self.board_.add_white_peg(Pos2D(DEFAULT_SIZE-1-i, j))
                self.board_.add_black_peg(Pos2D(i, j))

    def play(self):
        '''
        Joue la partie sur le plateau stocké en attribut.
        '''
        self.board_.print()
        current = 1
        while self.winner is None:
            current = 1-current
            self.players_[current].play()
            self.board_.print()
            print('')

    @property
    def winner(self):
        return self.board_.winner
