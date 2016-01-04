class Human(object):

    def __init__(self, player):
        self.player = player

    def action(self, board):
        print board
        opt = None
        while opt not in range(1, 10):
            opt = raw_input('Choice [1-9]: ')
            try:
                opt = int(opt)
            except ValueError:
                opt = None

        return opt - 1
