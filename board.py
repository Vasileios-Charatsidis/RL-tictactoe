import numpy as np


class Board(object):

    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = 2
    DRAW = 3

    FORMATTER = \
    "-------------\n" + \
    "| {0} | {1} | {2} |\n" + \
    "|-----------|\n" + \
    "| {3} | {4} | {5} |\n" + \
    "|-----------|\n" + \
    "| {6} | {7} | {8} |\n" + \
    "-------------"
    NAMES = [' ', 'X', 'O']

    def __init__(self):
        self.state = np.array([Board.EMPTY] * 9)

    def act(self, move, player):
        self.state[move] = player

    def get_valid(self):
        return np.where(self.state == Board.EMPTY)[0]

    def game_state(self):
        state_mat = self.state.reshape((3, 3))
        p1_win = [Board.PLAYER_X] * 3
        p2_win = [Board.PLAYER_O] * 3

        for i in range(3):
            # check rows
            row = state_mat[i, :]
            if np.all(row == p1_win) or np.all(row == p2_win):
                return state_mat[i, i]
            # check cols
            col = state_mat[:, i]
            if np.all(col == p1_win) or np.all(col == p2_win):
                return state_mat[i, i]
            
        # check first diagonal
        first_diag = state_mat.diagonal()
        if np.all(first_diag == p1_win) or np.all(first_diag == p1_win):
            return first_diag[0]
        # check second diagonal
        second_diag = np.fliplr(state_mat).diagonal()
        if np.all(second_diag == p1_win) or np.all(second_diag == p1_win):
            return second_diag[0]

        if len(state_mat == Board.EMPTY) > 0:
            return Board.EMPTY

        return Board.DRAW

    def __str__(self):
        return Board.FORMATTER.format(*[Board.NAMES[s] for s in self.state])

    def __len__(self):
        return len(self.state)

    @staticmethod
    def play(agent1, agent2, modulo = 1):
        board = Board()

        for i in range(9):
            agent = agent1 if i % 2 == 0 else agent2
            
            move = agent.action(board)
            board.act(move, agent.player)

            if modulo != None and i % modulo == 0:
                print '\nBoard', i, '\n', board, '\n'

            game_state = board.game_state()
            if game_state != Board.EMPTY:
                break

        return game_state, board
