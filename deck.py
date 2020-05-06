from typing import List
from card import Card


class Deck(object):

    def __str__(self):
        return str([card.card_text for card in self.cards])

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def draw_card(self):
        return self.cards.pop()
