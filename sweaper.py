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
mine_grid = [[choice(3 * [0] + [1]) for i in range(9)] for j in range(9)]
player_grid = [[-1 for i in range(9)] for j in range(9)]
print(mine_grid)