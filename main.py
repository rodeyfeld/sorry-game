import sys
from typing import List

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (220, 220, 220)


class Team(object):
    COLOR_CHOICES = [
        {"value": GREEN, "name": "GREEN"},
        {"value": BLUE, "name": "BLUE"},
        {"value": RED, "name": "RED"},
        {"value": YELLOW, "name": "YELLOW"},
    ]

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.start_point = None
        self.safe_point = None
        self.runway_points = []


class Player(object):

    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.pawns = []


class Point(object):
    color = WHITE

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class StandardPoint(Point):
    color = BLACK

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.occupied_by = None


class RunwayPoint(Point):

    def __init__(self, x: int, y: int, team: Team):
        super().__init__(x, y)
        self.team = team
        self.color = team.color
        self.occupied_by = None


class SafePoint(Point):

    def __init__(self, x: int, y: int, team: Team):
        super().__init__(x, y)
        self.team = team
        self.color = team.color
        self.num_pieces: int = 0


class StartPoint(Point):

    def __init__(self, x: int, y: int, team: Team):
        super().__init__(x, y)
        self.team = team
        self.color = team.color


class Pawn(object):
    PAWN_SIZE = 5
    PAWN_OFFSET = 5

    def __init__(self, player: Player, point: Point):
        self.player = player
        self.point = point


class Board(object):
    BOARD_START_X = 0
    BOARD_START_Y = 0
    BOARD_LENGTH = 15
    BOARD_WIDTH = 15
    POINT_SIZE = 30
    START_OFFSET = 4
    START_LENGTH = 1
    RUNWAY_LENGTH = 6
    SAFE_LENGTH = 6
    SAFE_OFFSET = 2

    def __init__(self, players):

        self.points: List[Point] = []
        self.start_points: List[StartPoint] = []

        for i in range(0, self.BOARD_LENGTH + 1):
            self.points.append(StandardPoint(x=i, y=self.BOARD_START_Y))
            self.points.append(StandardPoint(x=i, y=self.BOARD_LENGTH))
            self.points.append(StandardPoint(x=self.BOARD_WIDTH, y=i))
            self.points.append(StandardPoint(x=self.BOARD_START_X, y=i))

        start_coords = ((self.BOARD_START_X + self.START_OFFSET, self.BOARD_START_Y + self.START_LENGTH),
                        (self.BOARD_LENGTH - self.START_LENGTH, self.BOARD_START_Y + self.START_OFFSET),
                        (self.BOARD_LENGTH - self.START_OFFSET, self.BOARD_LENGTH - self.START_LENGTH),
                        (self.BOARD_START_X + self.START_LENGTH, self.BOARD_LENGTH - self.START_OFFSET),
                        )

        safe_coords = (((self.BOARD_START_X + self.SAFE_OFFSET, self.BOARD_START_Y + self.SAFE_LENGTH),
                        (self.BOARD_LENGTH - self.SAFE_LENGTH, self.BOARD_START_Y + self.SAFE_OFFSET),
                        (self.BOARD_LENGTH - self.SAFE_OFFSET, self.BOARD_LENGTH - self.SAFE_LENGTH),
                        (self.BOARD_START_X + self.SAFE_LENGTH, self.BOARD_LENGTH - self.SAFE_OFFSET),
                        ))

        runway_coords = ([], [], [], [])
        for i in range(1, self.RUNWAY_LENGTH):
            runway_coords[0].append((self.BOARD_START_X + self.SAFE_OFFSET, self.BOARD_START_Y + i))
            runway_coords[1].append((self.BOARD_LENGTH - i, self.BOARD_START_Y + self.SAFE_OFFSET))
            runway_coords[2].append((self.BOARD_LENGTH - self.SAFE_OFFSET, self.BOARD_LENGTH - i))
            runway_coords[3].append((self.BOARD_START_X + i, self.BOARD_LENGTH - self.SAFE_OFFSET))

        for index, player in enumerate(players):
            start_point = StartPoint(x=start_coords[index][0], y=start_coords[index][1], team=player.team)
            safe_point = SafePoint(x=safe_coords[index][0], y=safe_coords[index][1], team=player.team)
            player.team.start_point = start_point
            player.team.safe_point = safe_point
            self.points.append(start_point)
            self.points.append(safe_point)
            for runway_coord in runway_coords[index]:
                runway_point = RunwayPoint(x=runway_coord[0], y=runway_coord[1], team=player.team)
                player.team.runway_points.append(runway_point)
                self.points.append(runway_point)


class Game(object):

    def __init__(self):
        pygame.init()
        self.players: List[Player] = []
        self.create_players()
        self.board = Board(self.players)
        self.create_pawns()
        self.screen = pygame.display.set_mode([480, 480])
        self.screen.fill(WHITE)

    def draw_board(self):
        for point in self.board.points:
            new_rect = pygame.rect = (
                point.x * self.board.POINT_SIZE, point.y * self.board.POINT_SIZE, self.board.POINT_SIZE,
                self.board.POINT_SIZE)
            pygame.draw.rect(self.screen, point.color, new_rect, 1)

        for player in self.players:
            pawn_offset = Pawn.PAWN_OFFSET
            for pawn in player.pawns:
                new_rect = pygame.rect = (
                    pawn.point.x * self.board.POINT_SIZE + pawn_offset, pawn.point.y * self.board.POINT_SIZE +
                    pawn_offset, Pawn.PAWN_SIZE, Pawn.PAWN_SIZE
                )
                pygame.draw.rect(self.screen, player.team.color, new_rect, 1)
                pawn_offset += 5

    def create_players(self):
        for color_choice in Team.COLOR_CHOICES:
            team = Team(name=color_choice["name"], color=color_choice["value"])
            player = Player(name=team.name, team=team)
            self.players.append(player)

    def create_pawns(self):
        for player in self.players:
            print(player.team.safe_point)
            for i in range(0, 4):
                pawn = Pawn(player=player, point=player.team.safe_point)
                player.pawns.append(pawn)


game = Game()
game.draw_board()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
