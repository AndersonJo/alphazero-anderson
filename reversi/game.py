from time import sleep
from typing import List, Tuple, Union

import pygame
import numpy as np

from env import Game


class Reversi(Game):
    EMPTY = 0
    HINT = 1
    WHITE = 2
    BLACK = 3

    def __init__(self, board_width=8, board_height=8):
        assert board_width % 2 == 0, 'Board width should be an even number'
        assert board_height % 2 == 0, 'Board height should be an even number'
        assert board_width >= 4, 'Board width should be more than 4'
        assert board_height >= 4, 'Board height should be more than 4'

        self.board_width = board_width
        self.board_height = board_height
        self.board = None

        self.reset()

    def reset(self):
        if self.board is None:
            self.board = np.zeros((self.board_height, self.board_width), dtype=np.int8)
        else:
            self.board[:] = self.EMPTY

        x = self.board_width // 2
        y = self.board_height // 2

        self.board[x, y] = self.WHITE
        self.board[x - 1, y - 1] = self.WHITE
        self.board[x, y - 1] = self.BLACK
        self.board[x - 1, y] = self.BLACK

    def calculate_flippable_positions(self, x, y, player) -> Union[List[Tuple[int, int]], None]:
        """
        :param x: the index position of x
        :param y: the index position of y
        :param player: white or black (1, 2)
        :return a list of flippable positions where opponent's pieces are
        """
        x_position, y_position = x, y
        if player == self.WHITE:
            opponent = self.BLACK
        else:
            opponent = self.WHITE

        if self.board[x, y] != self.EMPTY or not self.is_on_board(x, y):
            return None

        # Temporarily set the position as the player's one.
        self.board[y_position, x_position] = player

        # Find flippable positions on which opponent's pieces
        flips = list()
        for dx, dy in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = x_position, y_position
            x += dx
            y += dy
            if self.is_on_board(x, y) and self.board[x, y] == opponent:
                x += dx
                y += dy

                if not self.is_on_board(x, y):
                    continue

                while self.board[x, y] == opponent:
                    x += dx
                    y += dy
                    if not self.is_on_board(x, y):
                        break

                if not self.is_on_board(x, y):
                    continue

                if self.board[x, y] == player:
                    while True:
                        x -= dx
                        y -= dy
                        if x == x_position and y == y_position:
                            break
                        flips.append((x, y))

        # Turn back the position as empty space
        self.board[y_position, x_position] = self.EMPTY

        if not flips:
            return None
        return flips

    def is_on_board(self, x, y):
        return 0 <= x < self.board_width and 0 <= y < self.board_height


class PyGameReversi(Reversi):
    GAME_WIDTH = 500
    GAME_HEIGHT = 500
    SPACE_PIXEL = 50
    GRID_COLOR = (30, 30, 30)

    WHITE_COLOR = (230, 230, 230)
    BLACK_COLOR = (30, 30, 30)
    HINT_COLOR = (200, 100, 0)

    def __init__(self, board_width=8, board_height=8):
        super(PyGameReversi, self).__init__(board_width, board_height)

        self.X_MARGIN = int(self.GAME_WIDTH - (self.board_width * self.SPACE_PIXEL) / 2)
        self.Y_MARGIN = int(self.GAME_HEIGHT - (self.board_height * self.SPACE_PIXEL) / 2)

        # Initialize PyGame
        pygame.init()
        pygame.display.set_caption('Reversi')
        clock = pygame.time.Clock()
        self.screen: pygame.Surface = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HEIGHT))
        self.screen.fill((125, 125, 125))

        font = pygame.font.Font('freesansbold.ttf', 16)
        bigfont = pygame.font.Font('freesansbold.ttf', 32)

    def render(self):
        # Draw grid lines of the board.
        for x in range(self.board_width + 1):
            # Draw the horizontal lines.
            startx = (x * self.SPACE_PIXEL) + self.X_MARGIN
            starty = self.Y_MARGIN
            endx = (x * self.SPACE_PIXEL) + self.X_MARGIN
            endy = self.Y_MARGIN + (self.board_height * self.SPACE_PIXEL)
            pygame.draw.line(self.screen, self.GRID_COLOR, (startx, starty), (endx, endy))
        for y in range(self.board_height + 1):
            # Draw the vertical lines.
            startx = self.X_MARGIN
            starty = (y * self.SPACE_PIXEL) + self.Y_MARGIN
            endx = self.X_MARGIN + (self.board_width * self.SPACE_PIXEL)
            endy = (y * self.SPACE_PIXEL) + self.Y_MARGIN
            pygame.draw.line(self.screen, self.GRID_COLOR, (startx, starty), (endx, endy))

        # Draw the black & white tiles or hint spots.
        for y in range(self.board_height):
            for x in range(self.board_width):
                centerx, centery = self._pixel_to_coord(x, y)
                if self.board[x, y] == self.WHITE or self.board[x, y] == self.BLACK:
                    if self.board[x, y] == self.WHITE:
                        color = self.WHITE_COLOR
                    else:
                        color = self.BLACK_COLOR
                    pygame.draw.circle(self.screen, color, (centerx, centery), int(self.SPACE_PIXEL / 2) - 4)
                if self.board[x, y] == self.HINT:
                    pygame.draw.rect(self.screen, self.HINT_COLOR, (centerx - 4, centery - 4, 8, 8))

    def _pixel_to_coord(self, x, y):
        center_x = self.X_MARGIN + x * self.SPACE_PIXEL + int(self.SPACE_PIXEL / 2)
        center_y = self.Y_MARGIN + y * self.SPACE_PIXEL + int(self.SPACE_PIXEL / 2)
        return center_x, center_y


def dev():
    reversi = PyGameReversi()
    reversi.render()
    sleep(4)

    print(reversi.board)


if __name__ == '__main__':
    dev()
