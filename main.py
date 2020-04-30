import sys
from typing import List

import pygame
import card_types

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

    def get_exit_point(self):
        if self.start_point.x == Board.BOARD_START_X + Board.START_LENGTH:
            return self.start_point.x - Board.START_LENGTH, self.start_point.y
        elif self.start_point.x == Board.BOARD_START_X + Board.START_OFFSET:
            return self.start_point.x, self.start_point.y - Board.START_LENGTH
        elif self.start_point.x == Board.BOARD_LENGTH - Board.START_LENGTH:
            return self.start_point.x + Board.START_LENGTH, self.start_point.y
        else:
            return self.start_point.x, self.start_point.y - Board.START_LENGTH


class Player(object):

    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.pawns = []
        self.cards = []

    def draw_card(self, deck):
        card_drawn = deck.pop()
        self.cards.append(card_drawn)
        return card_drawn

    def play_card(self, card, pawn):
        self.cards.remove(card)
        card_options = card['options']
        choice = card_options[0]
        value = card['value']
        if choice == "start":
            # Only start movement cards are 1 and 2
            exit_point = self.team.get_exit_point()
            if value == 1:
                pawn.move_pawn(exit_point)
            else:
                pawn.move_pawn(Board.find_pos(curr_pos=exit_point, value=1))
        elif choice == "move":
            pawn.move_pawn(Board.find_pos(curr_pos=pawn.point, value=value))


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

    def move_pawn(self, new_point):
        if not new_point.is_occupied:
            self.point = new_point


class Card(object):
    ALL_CARD_TYPES = card_types.CARD_TYPES

    def __init__(self, card_text: str, card_id: int):
        self.card_text = card_text
        self.card_id = card_id

    def handle_card_effect(self):
        if self.card_id == 1:
            return {
                'options': ['start', 'move'],
                'value': 1
            }


class Deck(object):

    def __init__(self, cards: List[Card]):
        self.cards = cards


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

        self.standard_points: List[StandardPoint] = []
        self.safe_points: List[SafePoint] = []
        self.start_points: List[StartPoint] = []
        self.runway_points: List[RunwayPoint] = []

        for i in range(0, self.BOARD_LENGTH + 1):
            self.standard_points.append(StandardPoint(x=i, y=self.BOARD_START_Y))
            self.standard_points.append(StandardPoint(x=i, y=self.BOARD_LENGTH))
            self.standard_points.append(StandardPoint(x=self.BOARD_WIDTH, y=i))
            self.standard_points.append(StandardPoint(x=self.BOARD_START_X, y=i))

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
            self.start_points.append(start_point)
            self.safe_points.append(safe_point)
            for runway_coord in runway_coords[index]:
                runway_point = RunwayPoint(x=runway_coord[0], y=runway_coord[1], team=player.team)
                player.team.runway_points.append(runway_point)
                self.runway_points.append(runway_point)

    def draw_point(self, point, screen):
        new_rect = pygame.rect = (
            point.x * self.POINT_SIZE, point.y * self.POINT_SIZE, self.POINT_SIZE,
            self.POINT_SIZE)
        pygame.draw.rect(screen, point.color, new_rect, 1)

    def draw_board(self, screen):

        for standard_point in self.standard_points:
            self.draw_point(standard_point, screen)
        for start_point in self.start_points:
            self.draw_point(start_point, screen)
        for safe_point in self.safe_points:
            self.draw_point(safe_point, screen)
        for runway_point in self.runway_points:
            self.draw_point(runway_point, screen)

    # TODO: Change return value to be a Point, not coordsd
    @staticmethod
    def find_pos(curr_pos, value):
        x, y = curr_pos
        # Top lanew
        if y == Board.BOARD_START_Y and x <= Board.BOARD_WIDTH:
            if value + x > Board.BOARD_WIDTH:
                new_x = Board.BOARD_WIDTH
                new_y = Board.BOARD_START_Y + value - x
            else:
                new_x = value + x
                new_y = y
        # Right lane
        elif x == Board.BOARD_WIDTH and y <= Board.BOARD_LENGTH:
            if value + y > Board.BOARD_LENGTH:
                new_x = Board.BOARD_WIDTH - value - x
                new_y = Board.BOARD_LENGTH
            else:
                new_x = value + x
                new_y = y
        # Bottom lane
        elif y == Board.BOARD_LENGTH and x >= Board.BOARD_START_X:
            if x - value < Board.BOARD_START_X:
                new_x = Board.BOARD_START_X
                new_y = Board.BOARD_LENGTH - value - x
            else:
                new_x = x - value
                new_y = y
        # Left lane
        else:
            if y - value < Board.BOARD_START_Y:
                new_x = y - value
                new_y = Board.BOARD_START_Y
            else:
                new_x = x
                new_y = y - value
        return new_x, new_y


class Game(object):

    def __init__(self):
        pygame.init()
        self.players: List[Player] = []
        self.create_players()
        self.board = Board(self.players)
        self.deck: Deck
        self.create_pawns()
        self.screen = pygame.display.set_mode([480, 480])
        self.screen.fill(WHITE)
        self.board.draw_board(self.screen)

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
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
