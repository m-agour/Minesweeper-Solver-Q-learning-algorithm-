from random import randint, choice

EMPTY = 0
MINE = 1
UNKNOWN = -1
FLAG = -2

states = {
    'empty': 0,
    'mine': 1,
    'unknown': 2,
    'flag': 3
}
# will i need flag?


# lets make zeros more than ones

class Sweeper:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.mines_grid = [[choice(3 * [0] + [1]) for i in range(self.h)] for j in range(self.w)]
        self.player_grid = [[-1 for x in range(self.h)] for y in range(self.w)]

    def count_neighbours(self, row, col):
        c = 0
        for i in range(row-1, row+2):
            for j in range(col - 1, col + 2):
                if (0 <= i <= 8) and (0 <= j <= 8):
                    if self.mines_grid[i][j] == MINE:
                        c += 1
        return c

    