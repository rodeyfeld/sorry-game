from player import Player


class Pawn(object):
    PAWN_SIZE = 5
    PAWN_OFFSET = 5

    def __str__(self):
        return "Pawn belonging to player" + str(self.player)

    def __init__(self, player: Player):
        self.player = player
