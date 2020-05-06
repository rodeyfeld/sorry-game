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

    def __str__(self):
        return self.name

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.start_point = None
        self.safe_point = None
        self.runway_points = []

