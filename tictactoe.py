#!/usr/bin/python

from board import Board
from agent import Agent
from human import Human

import sys
import getopt
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from pprint import pprint


def run_games(agent1, agent2, games, modulo, show_boards):
    results = []
    for run in range(games):
        game_state, board = Board.play(agent1, agent2, modulo)
        results.append(game_state)
        if show_boards:
            print 'Game %d ended %d\n%s' % (run, game_state, board)

    return results

def run_learning(agent1, agent2, trials, step, title, modulo, show_boards):
    raw_results = []
    aggregated_results = {}
    for i in range(trials / step):
        # switch roles
        if i == (trials / step) / 2:
            tmp = agent1.player
            agent1.player = agent2.player
            agent2.player = tmp

        r = run_games(agent1, agent2, step, modulo, show_boards)

        # replace result with switched player number
        if i >= (trials / step) / 2:
            for k, v in enumerate(r):
                if v == Board.PLAYER_O: r[k] = Board.PLAYER_X
                elif v == Board.PLAYER_X: r[k] = Board.PLAYER_O

        index = (i + 1) * step
        aggregated_results[index] = dict(map(lambda (k, v): (k, v / float(step)), Counter(r).items()))
        raw_results += r

    x = np.arange(0, trials, step)
    player_1_chart = plt.plot(x, map(lambda e: e.get(Board.PLAYER_X, .0), aggregated_results.values()), 'rs', label = 'Player 1')
    player_2_chart = plt.plot(x, map(lambda e: e.get(Board.PLAYER_O, .0), aggregated_results.values()), 'bs', label = 'Player 2')
    draw_chart = plt.plot(x, map(lambda e: e.get(Board.DRAW, .0), aggregated_results.values()), 'gs', label = 'Draw')
    plt.xticks(x)
    plt.legend()
    plt.title(title)
    plt.show()

    return raw_results, aggregated_results

def play_against_human():
    agent1 = Agent(Board.PLAYER_X)
    agent2 = Agent(Board.PLAYER_O)
    run_games(agent1, agent2, 100, None, False)

    human = Human(Board.PLAYER_O)
    Board.play(agent1, human, None, [False, True])

def menu():
    print '1 - Learning vs. Random'
    print '2 - Learning vs. Learning'
    print '3 - Play against agent'
    print 'q - Exit'
    opt = raw_input('Choice: ')

    if opt is '1':
        # learning vs. random
        agent1 = Agent(Board.PLAYER_X, verbose = verbose)
        agent2 = Agent(Board.PLAYER_O, verbose = verbose, epsilon = 1.0)
        raw_results_rdm, aggregated_results_rdm = run_learning(agent1, agent2, trials, step, 'Learning vs Random', modulo, show_boards)
    elif opt is '2':
        # learning vs. learning
        agent1 = Agent(Board.PLAYER_X, verbose = verbose)
        agent2 = Agent(Board.PLAYER_O, verbose = verbose)
        raw_results, aggregated_results = run_learning(agent1, agent2, trials, step, 'Learning vs Learning', modulo, show_boards)
    elif opt is '3':
        play_against_human()

    if opt is not 'q':
        menu()


if __name__ == '__main__':

    try:
        long_opts = ['verbose', 'modulo=', 'trials=', 'show-boards', 'step=']
        opts, args = getopt.getopt(sys.argv[1:], 'vm:t:bs:', long_opts)
    except getopt.GetoptError as err:
        print str(err)
        print 'Usage:', ' - '.join(long_opts)
        sys.exit(2)

    verbose = False
    modulo = None
    trials = 1000
    show_boards = False
    step = 10
    for opt, arg in opts:
        if opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-m', '--modulo'):
            modulo = int(arg)
        elif opt in ('-t', '--trials'):
            trials = int(arg)
        elif opt in ('-b', '--show-boards'):
            show_boards = True
        elif opt in ('-s', '--step'):
            step = int(arg)

    menu()
