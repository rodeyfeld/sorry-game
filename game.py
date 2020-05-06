from typing import List
from card_types import CARD_TYPES
from board import Board
from card import Card
from deck import Deck
from pawn import Pawn
from player import Player
from team import Team
import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (220, 220, 220)


class Game(object):

    def __init__(self):
        pygame.init()
        self.players: List[Player] = []
        self.create_players()
        self.board = Board(self.players)
        self.deck = Deck([])
        self.create_deck()
        self.create_pawns()
        self.screen = pygame.display.set_mode([480, 480])
        self.screen.fill(WHITE)
        self.draw_board(self.screen)

    def create_deck(self):
        for card_type in CARD_TYPES:
            for _ in range(0, 4):
                card = Card(card_effect=card_type["card_effect"],
                            card_text=card_type["card_text"],
                            card_id=card_type["card_id"])
                self.deck.cards.append(card)

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

    def draw_point(self, point, screen):
        new_rect = pygame.rect = (
            point.x * self.board.POINT_SIZE, point.y * self.board.POINT_SIZE, self.board.POINT_SIZE,
            self.board.POINT_SIZE)
        pygame.draw.rect(screen, point.color, new_rect, 1)

    def draw_pawn(self, point, pawn_offset, screen):
        new_rect = pygame.rect = (
            point.x * self.board.POINT_SIZE + pawn_offset, point.y * self.board.POINT_SIZE +
            pawn_offset, Pawn.PAWN_SIZE, Pawn.PAWN_SIZE
        )
        pygame.draw.rect(screen, point.occupied_by[0].player.team.color, new_rect, 1)

    def draw_board(self, screen):
        # TODO: Look into clearing only specific areas
        screen.fill(WHITE)
        for standard_point in self.board.standard_points:
            pawn_offset = Pawn.PAWN_OFFSET
            for _ in standard_point.occupied_by:
                self.draw_pawn(standard_point, pawn_offset, screen)
            self.draw_point(standard_point, screen)
            self.board.all_points.append(standard_point)
        for start_point in self.board.start_points:
            pawn_offset = Pawn.PAWN_OFFSET
            for _ in start_point.occupied_by:
                self.draw_pawn(start_point, pawn_offset, screen)
                pawn_offset += 5
            self.draw_point(start_point, screen)
        for safe_point in self.board.safe_points:
            pawn_offset = Pawn.PAWN_OFFSET
            for _ in safe_point.occupied_by:
                self.draw_pawn(safe_point, pawn_offset, screen)
                pawn_offset += 5
            self.draw_point(safe_point, screen)
        for runway_point in self.board.runway_points:
            pawn_offset = Pawn.PAWN_OFFSET
            for _ in runway_point.occupied_by:
                self.draw_pawn(runway_point, pawn_offset, screen)
            self.draw_point(runway_point, screen)
            self.board.all_points.append(runway_point)

    def handle_card_action(self, selected_point, card):
        print(card)
        choice = card.card_effect["options"][0]
        value = card.card_effect["value"]
        new_pos = (0, 0)

        if choice == "start":
            # Only start movement cards are 1 and 2
            team = selected_point.occupied_by[0].player.team
            exit_point = self.board.get_exit_point(team=team)
            pawn = team.start_point.occupied_by.pop()
            if value == 1:
                new_pos = exit_point
            else:
                new_pos = Board.find_new_pos(curr_pos=exit_point, value=1)
        elif choice == "move":
            pawn = selected_point.occupied_by[0]
            new_pos = Board.find_new_pos(curr_pos=selected_point, value=value)
        return new_pos, pawn
