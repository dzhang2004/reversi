"""
CMSC 14200, Spring 2023
Project
Reversi GUI implementation.

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""
import os
import sys
from typing import List, Dict, Tuple, Optional
import random

import pygame
import click
from reversi import Reversi

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


BoardGridType = List[List[Optional[int]]]

class ReversiGUI:
    """
    Class for a GUI-based Reversi game
    """

    window : int
    border : int
    player_color: Dict[int, Tuple[int, int, int]]
    reversi: Reversi
    surface: pygame.Surface
    clock : pygame.time.Clock

    def __init__(self, side: int, players: int = 2, othello: bool = True):
        """
        Constructor
        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
                configuration.
            window (int): height of window
            border (int) number of pixels to use as border around elements
        """

        assert 6 <= side <= 20
        assert 2 <= players <= 9
        self.window = 700
        self.border = 40

        self.player_color = {1: (0, 0, 0), 2: (255, 255, 255)}
        for i in range(3, players + 1):
            self.player_color[i] = (random.randint(0, 255), \
                                    random.randint(0, 255), \
                                    random.randint(0, 255))

        pygame.init()
        pygame.display.set_caption("ReversiGUI")
        self.reversi = Reversi(side, players, othello)
        self.grid = self.reversi.grid
        self.surface = pygame.display.set_mode((self.window, self.window))
        self.clock = pygame.time.Clock()
        self.title_screen()
        self.event_loop()


    @property
    def square(self) -> int:
        """
        The length of one side of a cell
        Args: none beyond self
        Returns (int): the length of one side of a cell
        """
        return (self.window - 2 * self.border) // len(self.grid)


    def draw_window(self) -> None:
        """
        Draws the contents of the window
        Args: none beyond self
        Returns: nothing
        """
        self.surface.fill((128, 128, 128))

        for row_i in range(len(self.grid)):
            for col_i in range(len(self.grid)):
                rectangle = (self.border + col_i * self.square, \
                    self.border + row_i * self.square, self.square, self.square)
                pygame.draw.rect(self.surface, color=(255, 255, 255), \
                                 rect=rectangle)
                pygame.draw.rect(
                    self.surface, color=(0, 0, 0), rect=rectangle, width=1)

        for (coord_row, coord_col) in self.reversi.available_moves:
            rectangle = (self.border + coord_col * self.square, \
                    self.border + coord_row * self.square, self.square, \
                        self.square)
            pygame.draw.rect(self.surface, color=(195, 195, 195), \
                             rect=rectangle)
            pygame.draw.rect(
                self.surface, color=(0, 0, 0), rect=rectangle, width=1)

        row: List[Optional[int]]
        cell: Optional[int]
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if isinstance(cell, int):
                    left = self.border + self.square // 2 + self.square * j
                    top = self.border + self.square // 2 + self.square * i
                    pygame.draw.circle(self.surface, color=(0, 0, 0), \
                        center=(left, top), radius=(self.square - 5)// 2)
                    pygame.draw.circle(self.surface, \
                        color=self.player_color[cell], center=(left, top),
                        radius=((self.square - 5)// 2) - 2)

        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        player_turn = font.render(f"Turn: Player {self.reversi.turn}", True, \
                                  self.player_color[self.reversi.turn])
        player_center = player_turn.get_rect(center=(
            self.border + self.square * len(self.grid) // 2, self.border // 2))
        self.surface.blit(player_turn, player_center)

        if self.reversi.done:
            self.surface.fill((128, 128, 128))
            font = pygame.font.Font(pygame.font.get_default_font(), 50)
            if len(self.reversi.outcome) == 1:
                winner_name = font.render(
                    f"Winner: Player {self.reversi.outcome[0]}", True, \
                        self.player_color[self.reversi.outcome[0]])
            else:
                winner_str = ', '.join(
                    str(player) for player in self.reversi.outcome)
                winner_name = font.render(
                    f"Winners: Players {winner_str}", True, (0, 0, 0))
            winner_center = winner_name.get_rect(center=(
                self.border + self.square * len(self.grid) // 2, \
                self.border + self.square * len(self.grid) // 2))
            self.surface.blit(winner_name, winner_center)

    def draw_title(self) -> None:
        """
        Draws the contents of the title screen
        Args: none beyond self
        Returns: nothing
        """
        self.surface.fill((0, 255, 0))
        t_font = pygame.font.Font(pygame.font.get_default_font(), 100)
        s_font = pygame.font.Font(pygame.font.get_default_font(), 50)
        title = t_font.render("Reversi", True, (0, 0, 0))
        start = s_font.render("Start Game", True, (0, 0, 0), (180, 180, 180))
        title_center = title.get_rect(
            center=(self.window // 2, self.window // 2))
        start_center = start.get_rect(
            center=(self.window // 2, self.window // 2 + 200))
        self.surface.blit(title, title_center)
        self.surface.blit(start, start_center)

    def title_screen(self) -> None:
        """
        Displays the title screen before playing the game
        Args: none beyond self
        Returns: nothing
        """
        s_font = pygame.font.Font(pygame.font.get_default_font(), 50)
        c_left, c_top = (self.window // 2, self.window // 2 + 200)
        width, height = s_font.size("Start Game")
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    left, top = event.pos
                    if (c_left - width // 2 <= left <= c_left + width // 2 and
                        c_top - height // 2 <= top <= c_top + width // 2):
                        self.event_loop()

            self.draw_title()
            pygame.display.update()

    def event_loop(self) -> None:
        """
        Handles user interactions
        Args: none beyond self
        Returns: nothing
        """
        pygame.mixer.music.load('Mission-Impossible.mp3')
        pygame.mixer.music.play(loops=-1)
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif self.reversi.done:
                    pygame.mixer.music.stop()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    left, top = event.pos
                    row = int((top - self.border) / self.square)
                    col = int((left - self.border) / self.square)
                    for cell_coordinate in self.reversi.available_moves:
                        r_val, c_val = cell_coordinate
                        if r_val == row and c_val == col:
                            self.grid[r_val][c_val] = self.reversi.turn
                            self.reversi.apply_move((row, col))

            self.reversi.load_game(self.reversi.turn, self.grid)
            self.draw_window()
            pygame.display.update()
            self.clock.tick(24)

@click.command("gui")
@click.option("-s", "--board-size", default=8, help='Size of the board.')
@click.option("-n", "--num-players", default=2, help='Number of players.')
@click.option("--othello/--non-othello", default=True, is_flag=True, \
            help='Specify whether to play in Othello mode or not')
def cmd(board_size, num_players, othello):
    """
    Initiates a GUI based on command-line parameters for the board size, number
    of players, and othello/non-othello flag
    """
    if (board_size % 2 == 1 and num_players % 2 == 0) or (
        board_size % 2 == 0 and num_players % 2 == 1):
        click.echo("Error Message: The parity of the players " \
                    "and board size doesn't match")
    else:
        ReversiGUI(board_size, num_players, othello)
if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
