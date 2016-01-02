#!/usr/bin/python

from board import Board
from agent import Agent

import sys
import getopt


def run_learning(agent1, agent2, trials, modulo, show_boards):
    results = {}
    for run in range(trials):
        game_state, board = Board.play(agent1, agent2, modulo)
        results[game_state] = results.get(game_state, 0) + 1
        if show_boards:
            print 'Game %d ended %d\n%s' % (run, game_state, board)

    return results


if __name__ == '__main__':

    try:
        long_opts = ['verbose', 'modulo=', 'trials=', 'show-boards']
        opts, args = getopt.getopt(sys.argv[1:], 'vm:t:b', long_opts)
    except getopt.GetoptError as err:
        print str(err)
        print 'Usage:', ' - '.join(long_opts)
        sys.exit(2)

    verbose = False
    modulo = None
    trials = 1000
    show_boards = False
    for opt, arg in opts:
        if opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-m', '--modulo'):
            modulo = int(arg)
        elif opt in ('-t', '--trials'):
            trials = int(arg)
        elif opt in ('-b', '--show-boards'):
            show_boards = True
    
    agent1 = Agent(Board.PLAYER_X, verbose = verbose)
    agent2 = Agent(Board.PLAYER_O, verbose = verbose)

    results = run_learning(agent1, agent2, trials, modulo, show_boards)

    for k, v in results.iteritems():
        print '%s\t%.3f' % (Board.NAMES[k], v / float(trials))


    agent1 = Agent(Board.PLAYER_X, verbose = verbose)
    agent2 = Agent(Board.PLAYER_O, verbose = verbose, epsilon = 1.0)

    results = run_learning(agent1, agent2, trials, modulo, show_boards)

    for k, v in results.iteritems():
        print '%s\t%.3f' % (Board.NAMES[k], v / float(trials))
