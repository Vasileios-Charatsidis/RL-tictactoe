#!/usr/bin/python

from board import Board
from agent import Agent

import sys
import getopt


if __name__ == '__main__':

    try:
        long_opts = ['verbose', 'modulo=']
        opts, args = getopt.getopt(sys.argv[1:], 'vm:', long_opts)
    except getopt.GetoptError as err:
        print str(err)
        print 'Usage:', ' - '.join(long_opts)
        sys.exit(2)

    verbose = False
    modulo = None
    for opt, arg in opts:
        if opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-m', '--modulo'):
            modulo = int(arg)
    
    agent1 = Agent(Board.PLAYER_X, verbose)
    agent2 = Agent(Board.PLAYER_O, verbose)

    for run in range(10):
        game_state, board = Board.play(agent1, agent2, modulo)
        print 'Game %d ended %d\n%s' % (run, game_state, board)
