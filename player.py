from typing import Dict, List


class Player(object):

    def __str__(self):
        return "Player: " + self.name

    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.cards: List = []

    def display_cards(self):
        return [card.card_text for card in self.cards]

    def add_card(self, card):
        self.cards.append(card)

    def play_card(self, card):
        return self.cards.remove(card)

