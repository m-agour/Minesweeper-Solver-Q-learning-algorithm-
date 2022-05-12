from time import sleep
import numpy as np
import pygame

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 40)

# screen t draw my minesweeper (3X3) for now since we are using Q-learning
SQUARE_WIDTH = 100
SQUARE_HEIGHT = 100
BOARDER = 50
BOARDER_TITLE = 50

rewards = {
    'lose': -1,
    'win': 1,
    'random': -0.3,
    'ideal': -0.2,
    'useless': -2,
}
# for drAWING
UNKNOWN_VALUE = -1
MINE_VALUE = -2

# only needed in case of winning or losing for drawing purposes.
FLAG_VALUE = -3
RED_MINE_VALUE = -4

states = {
    'mine': 1,
    'unknown': -1
}

shapes = {
    0: pygame.image.load("assets/0.png"),
    1: pygame.image.load("assets/1.png"),
    2: pygame.image.load("assets/2.png"),
    3: pygame.image.load("assets/3.png"),
    UNKNOWN_VALUE: pygame.image.load("assets/facingDown.png"),
    MINE_VALUE: pygame.image.load("assets/mine.png"),
    RED_MINE_VALUE: pygame.image.load("assets/lose.png"),
    FLAG_VALUE: pygame.image.load("assets/flagged.png"),
    'click': pygame.image.load("assets/click.png")
}


# todo: levels easy, med, hard or just leave bombs num as a measurement


class Sweeper:
    def __init__(self, w, h, mines_num):
        self.w = w
        self.h = h
        self.area = w * h
        self.size = self.w * self.h
        self.screen = pygame.display.set_mode([SQUARE_WIDTH * w + BOARDER, SQUARE_HEIGHT * h + BOARDER + BOARDER_TITLE])
        self.mines_num = mines_num
        self.player_grid = self.init_player_grid()
        self.mines_grid = self.init_mines_grid()
        self.progress = 0
        self.wins = 0
        self.last_clicked = None
        self.footage = []
        self.moves = 0

    def init_player_grid(self):
        return np.ones(self.w * self.h, dtype=np.int8) * UNKNOWN_VALUE

    def init_mines_grid(self):
        grid = np.concatenate((np.zeros(self.w * self.h - self.mines_num, dtype=np.int8),
                               np.ones(self.mines_num, dtype=np.int8)), axis=0) * MINE_VALUE
        np.random.shuffle(grid)
        return grid

    def count_neighbours(self, x, y):
        c = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (0 <= i < self.w) and (0 <= j < self.h):
                    if self.mines_grid[j * self.w + i] == MINE_VALUE:
                        c += 1
        return c

    def reveal_neighbours(self, x, y):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (0 <= i < self.w) and (0 <= j < self.h) and not (i == x and j == y):
                    if (self.player_grid[j * self.w + i] == UNKNOWN_VALUE) and (
                            self.mines_grid[j * self.w + i] == 0):
                        count = self.count_neighbours(i, j)
                        self.player_grid[j * self.w + i] = count
                        if count == 0:
                            self.reveal_neighbours(i, j)
                    else:
                        continue

    def get_neighbours(self, x, y):
        n = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (0 <= i < self.w) and (0 <= j < self.h) and not (i == x and j == y):
                    n.append(self.player_grid[i + self.w * j])

        return np.array(n)

    def reveal(self, i):
        self.moves += 1
        y = i // self.w
        x = i % self.w
        self.last_clicked = (x, y)
        reward = rewards['lose']
        done = False
        last_state = np.copy(self.player_grid)

        neighbours = self.get_neighbours(x, y)
        if self.mines_grid[y * self.w + x] == MINE_VALUE:
            reward = rewards['lose']
            # replace mine shape
            self.player_grid[np.where(self.mines_grid == MINE_VALUE)] = MINE_VALUE
            self.player_grid[y * self.w + x] = RED_MINE_VALUE
            s = 'lose\n'
            done = True

        elif self.player_grid[y * self.w + x] == UNKNOWN_VALUE:
            count = self.count_neighbours(x, y)
            self.player_grid[y * self.w + x] = count
            if count == 0:
                self.reveal_neighbours(x, y)

            if self.is_won():
                reward = rewards['win']
                s = 'win\n'
                done = True
                # replace unopened with a flag (mines)
                self.player_grid[self.player_grid == UNKNOWN_VALUE] = FLAG_VALUE
                self.progress += 1
                self.wins += 1

            elif np.count_nonzero(neighbours == UNKNOWN_VALUE) == len(neighbours):
                s = 'random'
                reward = rewards['random']

            else:
                reward = rewards['ideal']
                s = 'ideal'

                self.progress += 1

        elif not len(np.flatnonzero((last_state != self.player_grid))):
            s = 'useless'
            reward = rewards['useless']
        return self.get_encoded_state(), reward, done

    def display(self, t, save_name=None, episode=None):
        if self.last_clicked:
            x, y = self.last_clicked
            self.screen.blit(pygame.transform.scale(shapes['click'], (70, 70)),
                             (BOARDER/2 + x * 100 + 15, BOARDER/2 + y * 100 + 15 + BOARDER_TITLE))
            pygame.display.flip()
            if save_name:
                pygame.image.save(self.screen, 'footage/' + save_name + '0.jpg')
            sleep(0.3 * t)

        self.screen.fill((150, 150, 150))
        self.screen.blit(font.render(f'Episode: {episode}', True, (19, 11, 16)), (BOARDER, BOARDER/3))
        for j in range(self.h):
            for i in range(self.w):
                value = self.player_grid[j * self.w + i]
                self.screen.blit(pygame.transform.scale(shapes[value], (100, 100)),
                                 (BOARDER/2 + i * 100, BOARDER/2 + j * 100 + BOARDER_TITLE))
        pygame.display.flip()
        if save_name:
            pygame.image.save(self.screen, 'footage/' + save_name + '1.jpg')
        sleep(0.6 * t)

    def is_won(self):
        return np.count_nonzero(self.player_grid == UNKNOWN_VALUE) == self.mines_num

    def reset(self):
        self.progress = 0
        self.moves = 0
        self.player_grid = self.init_player_grid()
        self.mines_grid = self.init_mines_grid()
        self.last_clicked = None

    def get_DQN_state(self):
        DQN_state = self.player_grid.astype(np.int8) / 8
        DQN_state = DQN_state.astype(np.float16)
        return DQN_state.reshape((self.w, self.h, 1))

    def get_state(self):
        return self.player_grid

    def get_actions(self):
        return [i for i, x in enumerate(self.player_grid) if x == UNKNOWN_VALUE]

    def get_encoded_state(self):
        modified_state = [i + 1 for i in self.player_grid]

        try:
            return np.ravel_multi_index(modified_state, np.ones(self.area, dtype='uint8') * self.mines_num + 2)
        except:
            # print(self.player_grid, modified_state)
            return None
