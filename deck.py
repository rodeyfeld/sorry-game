from typing import List
from card import Card


class Deck(object):

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def draw_card(self):
        return self.cards.pop()
