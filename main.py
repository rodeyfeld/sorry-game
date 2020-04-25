import sys
from typing import List

import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Tile(object):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.occupied_by = None


class RunwayTile(Tile):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.color = GREEN


class Board(object):

    BOARD_START_X = 0
    BOARD_START_Y = 0
    BOARD_LENGTH = 15
    BOARD_WIDTH = 15
    TILE_SIZE = 30

    def __init__(self):
        self.points: List[Tile] = []
        for i in range(0, self.BOARD_LENGTH+1):
            self.points.append(Tile(x=i, y=self.BOARD_START_Y))
            self.points.append(Tile(x=i, y=self.BOARD_LENGTH))
            self.points.append(Tile(x=self.BOARD_WIDTH, y=i))
            self.points.append(Tile(x=self.BOARD_START_X, y=i))


class Game(object):

    def __init__(self):
        pygame.init()
        self.board = Board()
        self.screen = pygame.display.set_mode([500, 500])
        self.screen.fill(WHITE)

    def draw_board(self):
        for point in self.board.points:
            print(point.x, point.y)
            new_tile = pygame.rect = (point.x*self.board.TILE_SIZE, point.y*self.board.TILE_SIZE, self.board.TILE_SIZE, self.board.TILE_SIZE)
            pygame.draw.rect(self.screen, BLACK, new_tile, 1)


game = Game()
game.draw_board()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
