from board import Board

import random
from copy import deepcopy


class Agent(object):

    def __init__(self, player, epsilon = 0.1, verbose = False):
        self.player = player
        self.verbose = verbose
        self.epsilon = epsilon
        self.alpha = 0.95
        self.loose_reward = 0

        self.values = {}
        self.prev_board = None
        self.prev_value = 0

    def action(self, board):
        self.log('valid moves', board.get_valid())

        if random.random() > self.epsilon:
            # greedy action
            move, value = self.greedy(board)
        else:
            # exploratory action
            move, value = self.random(board)

        board.act(move, self.player)
        self.log('moved', move)

        self.prev_board = deepcopy(board)
        self.prev_value = value
        return move

    def greedy(self, board):
        max_value = -1
        max_move = None

        for move in board.get_valid():
            board.act(move, self.player)
            value = self.lookup(board)
            if value > max_value:
                max_value = value
                max_move = move
            board.act(move, Board.EMPTY)

        self.backup(max_value)
        return max_move, max_value

    def lookup(self, board):
        state_tpl = tuple(board.state)
        if not state_tpl in self.values:
            self.add(board)
        return self.values[state_tpl]

    def add(self, board):
        game_state = board.game_state()
        state_tpl = tuple(board.state)
        reward = self.reward(game_state)
        self.log('adding {0} -> {1}'.format(state_tpl, reward))
        self.values[state_tpl] = reward

    def reward(self, game_state):
        if game_state == self.player:
            return 1
        elif game_state == Board.EMPTY:
            return 0.5
        elif game_state == Board.DRAW:
            return 0
        else:
            return self.loose_reward

    def backup(self, next_value):
        if self.prev_board is not None:
            prev_state = tuple(self.prev_board.state)
            delta = self.alpha * (next_value - self.prev_value)
            self.log('backing up', prev_state, 'by', delta)
            self.values[prev_state] += delta

    def random(self, board):
        move = random.choice(board.get_valid())
        board.act(move, self.player)
        value = self.lookup(board)
        return move, value

    def log(self, *what):
        if self.verbose:
            s = 'Player ' + str(self.player) + ':'
            print s, ' '.join(map(str, list(what)))
