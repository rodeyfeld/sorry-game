from typing import List

import pygame

from pawn import Pawn
from point import StandardPoint, SafePoint, StartPoint, RunwayPoint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (220, 220, 220)


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

    def move_piece(self, coords, pawn):
        x, y = coords
        new_point = self.get_point(x=x, y=y)
        new_point.occupied_by.append(pawn)

    def get_point(self, x, y):
        # TODO: Refactor to use more efficient method of finding points
        for point in self.all_points:
            if point.x == x and point.y == y:
                return point
        return None

    @staticmethod
    def get_exit_point(team):
        if team.start_point.x == Board.BOARD_START_X + Board.START_LENGTH:
            return team.start_point.x - Board.START_LENGTH, team.start_point.y
        elif team.start_point.x == Board.BOARD_START_X + Board.START_OFFSET:
            return team.start_point.x, team.start_point.y - Board.START_LENGTH
        elif team.start_point.x == Board.BOARD_LENGTH - Board.START_LENGTH:
            return team.start_point.x + Board.START_LENGTH, team.start_point.y
        else:
            return team.start_point.x, team.start_point.y - Board.START_LENGTH

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
