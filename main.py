import sys
from time import sleep
from typing import List, Dict

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

    def draw_card(self, card):
        self.cards.append(card)

    def play_card(self, card, curr_point):
        self.cards.remove(card)
        choice = card.card_effect['options'][0]
        value = card.card_effect['value']
        new_pos = (0, 0)

        if choice == "start":
            # Only start movement cards are 1 and 2
            exit_point = self.team.get_exit_point()
            pawn = self.team.start_point.occupied_by.pop()
            print(self.team.start_point.occupied_by)
            if value == 1:
                new_pos = exit_point
            else:
                new_pos = Board.find_new_pos(curr_pos=exit_point, value=1)


        # elif choice == "move":
        #     pawn.move_pawn(Board.find_new_pos(curr_pos=pawn.point, value=value))
        return pawn, new_pos


class Point(object):
    color = WHITE

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class StandardPoint(Point):
    color = BLACK

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.occupied_by = []


class RunwayPoint(Point):

    def __init__(self, x: int, y: int, team: Team):
        super().__init__(x, y)
        self.team = team
        self.color = team.color
        self.occupied_by = []


class SafePoint(Point):

    def __init__(self, x: int, y: int, team: Team):
        super().__init__(x, y)
        self.team = team
        self.color = team.color
        self.occupied_by = []


class StartPoint(Point):

    def __init__(self, x: int, y: int, team: Team):
        super().__init__(x, y)
        self.team = team
        self.color = team.color
        self.occupied_by = []


class Pawn(object):
    PAWN_SIZE = 5
    PAWN_OFFSET = 5

    def __init__(self, player: Player):
        self.player = player


class Card(object):
    ALL_CARD_TYPES = card_types.CARD_TYPES

    def __init__(self, card_text: str, card_id: int, card_effect: Dict):
        self.card_text = card_text
        self.card_id = card_id
        self.card_effect = card_effect

    # def handle_card_effect(self):
    #     if self.card_id == 1:
    #         return {
    #             'options': ['start', 'move'],
    #             'value': 1
    #         }


class Deck(object):

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def draw_card(self):
        return self.cards.pop()


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

        self.all_points = []
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

    def draw_pawn(self, point, pawn_offset, screen):
        new_rect = pygame.rect = (
            point.x * self.POINT_SIZE + pawn_offset, point.y * self.POINT_SIZE +
            pawn_offset, Pawn.PAWN_SIZE, Pawn.PAWN_SIZE
        )
        pygame.draw.rect(screen, point.occupied_by[0].player.team.color, new_rect, 1)

    def move_pice(self, coords, pawn):
        x, y = coords
        new_point = self.get_point(x=x, y=y)
        new_point.occupied_by.append(pawn)

    def draw_board(self, screen):
        # TODO: Look into clearing only specific areas
        screen.fill(WHITE)
        for standard_point in self.standard_points:
            pawn_offset = Pawn.PAWN_OFFSET
            for _ in standard_point.occupied_by:
                self.draw_pawn(standard_point, pawn_offset, screen)
            self.draw_point(standard_point, screen)
            self.all_points.append(standard_point)
        for start_point in self.start_points:
            print(start_point.occupied_by)
            pawn_offset = Pawn.PAWN_OFFSET
            for _ in start_point.occupied_by:
                self.draw_pawn(start_point, pawn_offset, screen)
                pawn_offset += 5
            self.draw_point(start_point, screen)
        for safe_point in self.safe_points:
            pawn_offset = Pawn.PAWN_OFFSET
            for _ in safe_point.occupied_by:
                self.draw_pawn(safe_point, pawn_offset, screen)
                pawn_offset += 5
            self.draw_point(safe_point, screen)
        for runway_point in self.runway_points:
            pawn_offset = Pawn.PAWN_OFFSET
            for _ in runway_point.occupied_by:
                self.draw_pawn(runway_point, pawn_offset, screen)
            self.draw_point(runway_point, screen)
            self.all_points.append(runway_point)

    def get_point(self, x, y):
        # TODO: Refactor to use more efficient method of finding points
        for point in self.all_points:
            if point.x == x and point.y == y:
                return point
        return None

    # TODO: Change return value to be a Point, not coords
    @staticmethod
    def find_new_pos(curr_pos, value):
        x, y = curr_pos
        # Top lane
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
        self.deck = self.create_deck()
        self.create_pawns()
        self.screen = pygame.display.set_mode([480, 480])
        self.screen.fill(WHITE)
        self.board.draw_board(self.screen)

        # for player in self.players:
        #     pawn_offset = Pawn.PAWN_OFFSET
        #     for pawn in player.pawns:
        #         new_rect = pygame.rect = (
        #             pawn.point.x * self.board.POINT_SIZE + pawn_offset, pawn.point.y * self.board.POINT_SIZE +
        #             pawn_offset, Pawn.PAWN_SIZE, Pawn.PAWN_SIZE
        #         )
        #         pygame.draw.rect(self.screen, player.team.color, new_rect, 1)
        #         pawn_offset += 5

    def create_deck(self):
        # todo: generate all cards
        card = Card("start", 1, {'options': ['start', 'move'], 'value': 1})
        cards = [card]
        deck = Deck(cards)
        return deck

    def create_players(self):
        for color_choice in Team.COLOR_CHOICES:
            team = Team(name=color_choice["name"], color=color_choice["value"])
            player = Player(name=team.name, team=team)
            self.players.append(player)

    def create_pawns(self):
        for player in self.players:
            print(player.team.safe_point)
            for i in range(0, 4):
                pawn = Pawn(player=player)
                player.team.start_point.occupied_by.append(pawn)
                player.pawns.append(pawn)



game = Game()
player_one = game.players[0]
player_one.draw_card(game.deck.draw_card())
pawn, new_pos = player_one.play_card(player_one.cards[0], curr_point=player_one.team.start_point)
game.board.move_pice(new_pos, pawn)
game.board.draw_board(game.screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
