from team import Team

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (220, 220, 220)


class Point(object):
    color = WHITE

    def __str__(self):
        return str(self.x) + ', ' + str(self.y)

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class StandardPoint(Point):
    color = BLACK

    def __str__(self):
        super().__str__()

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.occupied_by = []


class RunwayPoint(Point):

    def __str__(self):
        return str(self.x) + ', ' + str(self.y) + ": " + str(self.occupied_by) + "(" + self.team.name + ")"

    def __init__(self, x: int, y: int, team: Team):
        super().__init__(x, y)
        self.team = team
        self.color = team.color
        self.occupied_by = []


class SafePoint(Point):

    def __str__(self):
        return str(self.x) + ', ' + str(self.y) + ": " + str(self.occupied_by) + "(" + self.team.name + ")"

    def __init__(self, x: int, y: int, team: Team):
        super().__init__(x, y)
        self.team = team
        self.color = team.color
        self.occupied_by = []


class StartPoint(Point):

    def __str__(self):
        return str(self.x) + ', ' + str(self.y) + ": " + str(self.occupied_by) + "(" + self.team.name + ")"

    def __init__(self, x: int, y: int, team: Team):
        super().__init__(x, y)
        self.team = team
        self.color = team.color
        self.occupied_by = []

