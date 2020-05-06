import sys
from time import sleep
from typing import List, Dict

from game import Game
import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (220, 220, 220)

game = Game()
player_one = game.players[0]
player_one.add_card(game.deck.draw_card())
card = player_one.cards[0]
player_one.play_card(card=player_one.cards[0])
new_pos, pawn = game.handle_card_action(player_one.team.start_point, card)
print(new_pos)
game.board.move_pice(new_pos, pawn)
game.draw_board(game.screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
