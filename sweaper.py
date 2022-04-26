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

    def count_neighbours(self, x, y):
        c = 0
        for i in range(x-1, y+2):
            for j in range(x - 1, y + 2):
                if (0 <= i <= 8) and (0 <= j <= 8):
                    if self.mines_grid[i][j] == MINE:
                        c += 1
        return c

    def reveal(self, x, y):
        if self.mines_grid[x][y] == MINE:
            print("BOOM!")
        elif self.player_grid[x][y] == UNKNOWN:
            self.player_grid[x][y] = self.count_neighbours(x, y)

            # Can this be recursive?
            cells = [(x, y)]
            while len(cells) > 0:
                cell = cells.pop()
                x = cell[0]
                y = cell[1]
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        if (0 <= i <= 8) and (0 <= j <= 8):
                            if (self.player_grid[i][j] == UNKNOWN) and (self.mines_grid[i][j] == EMPTY):
                                self.player_grid[i][j] = self.count_neighbours(i, j)
                                if self.count_neighbours(i, j) == EMPTY and (i, j) not in cells:
                                    cells.append((i, j))
                                else:
                                    self.player_grid[i][j] = self.count_neighbours(i, j)



