from random import randint, choice, seed
seed(8)

states = {
    'empty': 0,
    'mine': 1,
    'unknown': -1,
}

# todo: levels easy, med, hard


class Sweeper:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.mines_grid = [[choice(3 * [0] + [1]) for i in range(self.h)] for j in range(self.w)]
        self.player_grid = [[-1 for x in range(self.h)] for y in range(self.w)]

    def count_neighbours(self, x, y):
        c = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (0 <= i < self.w) and (0 <= j < self.h):
                    if self.mines_grid[i][j] == states['mine']:
                        c += 1
        return c

    def reveal_neighbours(self, x, y):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (0 <= i < self.w) and (0 <= j < self.h) and not (i == x and j == y):
                    if (self.player_grid[i][j] == states['unknown']) and (
                            self.mines_grid[i][j] == states['empty']):
                        count = self.count_neighbours(i, j)
                        self.player_grid[i][j] = count
                        if count == 0:
                            self.reveal_neighbours(i, j)

                    else:
                        continue

    def reveal(self, x, y):
        if self.mines_grid[x][y] == states['mine']:
            print("You Lose!")
        elif self.player_grid[x][y] == states['unknown']:
            count = self.count_neighbours(x, y)
            self.player_grid[x][y] = count
            if count == 0:
                self.reveal_neighbours(x, y)



    def display(self):
        symbols = {-2: "F", -1: "."}
        for i in range(len(self.player_grid)):
            for j in range(len(self.player_grid[i])):
                value = self.player_grid[i][j]
                if value in symbols:
                    symbol = symbols[value]
                else:
                    symbol = str(value)
                print(f"{symbol} ", end='')
            print("")



    def display_mines(self):
        symbols = {-2: "F", -1: "."}
        for i in range(len(self.mines_grid)):
            for j in range(len(self.mines_grid[i])):
                value = self.mines_grid[i][j]
                if value in symbols:
                    symbol = symbols[value]
                else:
                    symbol = str(value)
                print(f"{symbol} ", end='')
            print("")


s = Sweeper(19, 19)
# s.reveal(8, 8)
s.reveal(10, 6)
# s.reveal(0, 5)
s.display()
print('-----------------')
s.display_mines()
