from enum import Enum
from motor_control import MotorController

IN_PER_SEC = 150.0
FAST_FEED_RATE = 5 * IN_PER_SEC
SLOW_FEED_RATE = 1 * IN_PER_SEC

class PieceType(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

class Team(Enum):
    WHITE = 1
    BLACK = 2

class Piece:
    def __init__(self, type, team):
        self.type = type
        self.team = team

class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.cnc = MotorController()
        pieceOrder = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,\
            PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]
        for i in range(8):
            self.grid[0][i] = Piece(pieceOrder[i], BLACK)
            self.grid[1][i] = Piece(PieceType.PAWN, BLACK)
            self.grid[6][i] = Piece(PieceType.PAWN, WHITE)
            self.grid[7][i] = Piece(pieceOrder[i], WHITE)
    def move_piece(startX, startY, endX, endY):
        if not is_move_legal(startX, startY, endX, endY):
            return False
        if self.grid[endX][endY] != None:
            self.cnc.move_to(endX, endY, FAST_FEED_RATE)
            self.cnc.kill_piece()

        self.cnc.move_to(startX, startY, FAST_FEED_RATE)
        self.cnc.engage_magnet(True)
        if startX == endX or startY == endY or abs(startY - endY) == abs(startX - endX):
            # if moving horizontally, vertically, or diagonally
            self.cnc.move_to(endX, endY, SLOW_FEED_RATE)
        else if abs(startX - endX) == 1 and abs(startY - endY) == 2:
            self.cnc.move_to(0.5 * (startX + endX), startY, SLOW_FEED_RATE)
            self.cnc.move_to(0.5 * (startX + endX), endY, SLOW_FEED_RATE)
            self.cnc.move_to(endX, endY, SLOW_FEED_RATE)
        else if abs(startX - endX) == 1 and abs(startY - endY) == 2:
            self.cnc.move_to(startX, (startY + endY) * 0.5, SLOW_FEED_RATE)
            self.cnc.move_to(endX, (startY + endY) * 0.5, SLOW_FEED_RATE)
            self.cnc.move_to(endX, endY, SLOW_FEED_RATE)
        else:
            self.cnc.engage_magnet(False)
            return False
        self.cnc.engage_magnet(False)

        self.grid[endX][endY] = self.grid[startX][startY]
        self.grid[startX][startY] = None

        return True

    def is_move_legal(startX, startY, endX, endY):
        # TODO make work properly
        if startX == endX or startY == endY or abs(startY - endY) == abs(startX - endX):
            return True
        else if abs(startX - endX) == 1 and abs(startY - endY) == 2:
            return True
        else if abs(startX - endX) == 1 and abs(startY - endY) == 2:
            return True
        else:
            return False
