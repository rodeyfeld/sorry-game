from typing import Dict

import card_types


class Card(object):

    ALL_CARD_TYPES = card_types.CARD_TYPES

    def __str__(self):
        return "Card: " + str(self.card_effect)

    def __init__(self, card_text: str, card_id: int, card_effect: Dict):
        self.card_text = card_text
        self.card_id = card_id
        self.card_effect = card_effect
