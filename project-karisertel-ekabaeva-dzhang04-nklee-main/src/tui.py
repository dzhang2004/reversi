"""
TUI of the reversi game
"""
from typing import List, Tuple
import click
from termcolor import colored
from reversi import ReversiBase, Reversi

WALL_CHARS = {
    "H_WALL": "─", "V_WALL": "│", "HV_WALL": "┼",
    "NW_CORNER": "┌", "NE_CORNER": "┐", "SW_CORNER": "└", "SE_CORNER": "┘",
    "VE_WALL": "├", "VW_WALL": "┤", "HS_WALL": "┬", "HN_WALL": "┴",
    "N_WALL": "╵", "E_WALL": "╶", "S_WALL": "╷", "W_WALL": "╴"
}

CLOCK_CHARS = {
    (False, False, False, False): " ",
    (False, False, False, True): WALL_CHARS["W_WALL"],
    (False, False, True, False): WALL_CHARS["S_WALL"],
    (False, False, True, True): WALL_CHARS["NE_CORNER"],
    (False, True, False, False): WALL_CHARS["E_WALL"],
    (False, True, False, True): WALL_CHARS["H_WALL"],
    (False, True, True, False): WALL_CHARS["NW_CORNER"],
    (False, True, True, True): WALL_CHARS["HS_WALL"],
    (True, False, False, False): WALL_CHARS["N_WALL"],
    (True, False, False, True): WALL_CHARS["SE_CORNER"],
    (True, False, True, False): WALL_CHARS["V_WALL"],
    (True, False, True, True): WALL_CHARS["VW_WALL"],
    (True, True, False, False): WALL_CHARS["SW_CORNER"],
    (True, True, False, True): WALL_CHARS["HN_WALL"],
    (True, True, True, False): WALL_CHARS["VE_WALL"],
    (True, True, True, True): WALL_CHARS["HV_WALL"]
}

PLAY_OPTION = "•"

PLAYER_COLOR = {1: "blue", 2: "red", 3: "yellow", 4: "green", 5: "cyan",
                6: "light_cyan", 7: "magenta", 8: "light_yellow",
                9: "dark_grey"}

def adj_walls(grid: List[List[str]],
              pos: Tuple[int, int]) -> Tuple[bool, bool, bool, bool]:
    """
    Checks for walls adjacent to the current wall we are looking at
    Args:
        grid (List[List[str]]): string grid representation of the maze
        at (Tuple[int, int]): position in our to_str grid at grid[row][col] 
    Returns:
        Tuple[bool, bool, bool, bool]: Presence of walls in the format of
            North, East, South, West. True if there is a wall in that
            direction, False if not
    """
    row, col = pos
    max_r, max_c = len(grid) - 1, len(grid[0]) - 1

    if row == 0 or grid[row - 1][col] == " ":
        north = False
    else:
        north = True

    if col == max_c or grid[row][col + 1] == " ":
        east = False
    else:
        east = True

    if row == max_r or grid[row + 1][col] == " ":
        south = False
    else:
        south = True

    if col == 0 or grid[row][col - 1] == " ":
        west = False
    else:
        west = True

    return north, east, south, west

def print_board(reversi: ReversiBase) -> None:
    """
    Prints the board of an ongoing reversi game

    Args:
        reversi (ReversiBase): reversi game
    """
    grid = reversi.grid
    side_length = len(grid) * 2 + 1
    str_grid = [[" "] * side_length for _ in range(side_length)]
    for i, row in enumerate(grid):
        for j, piece in enumerate(row):
            if piece is not None:
                str_grid[2 * i + 1][2 * j + 1] = colored(str(piece),
                                                         PLAYER_COLOR[piece])
            if i == 0:
                str_grid[i][2 * j + 1] = CLOCK_CHARS[(False, True, False, True)]
            if j == 0:
                str_grid[2 * i + 1][j] = CLOCK_CHARS[(True, False, True, False)]

            str_grid[2 * i + 2][2 * j + 1] = CLOCK_CHARS[(False, True,
                                                          False, True)]
            str_grid[2 * i + 1][2 * j + 2] = CLOCK_CHARS[(True, False,
                                                          True, False)]

    for i in range(0, side_length, 2):
        for j in range(0, side_length, 2):
            str_grid[i][j] = CLOCK_CHARS[adj_walls(str_grid, (i, j))]

    for (i, j) in reversi.available_moves:
        str_grid[2 * i + 1][2 * j + 1] = colored(PLAY_OPTION, attrs=["blink"])

    grid_rows = list(map("".join, str_grid))
    print("\n".join(grid_rows))

@click.command("play board")
@click.option("-n", "--num-players", default=2)
@click.option("-s", "--board-size", default=8)
@click.option("--othello/--non-othello", default=True, is_flag=True)
def start_tui(num_players, board_size, othello):
    """
    Begins the TUI for the game
    """
    reversi_game = Reversi(board_size, num_players, othello)
    display_board = True
    while not reversi_game.done:
        player_dict = {}
        if display_board:
            print_board(reversi_game)
        print(f"It is Player {reversi_game.turn}'s turn. "
              "Please choose a move:\n")
        for i, move in enumerate(reversi_game.available_moves):
            player_dict[i + 1] = move
            row, col = move
            print(f"{i + 1}) {row}, {col}")
        player_move = input()
        try:
            player_move = int(player_move)
            reversi_game.apply_move(player_dict[player_move])
        except ValueError:
            print("Error: Provided input cannot convert to move. Halting Game.")
            return
        except KeyError:
            print("Inputted move is not in the list of available moves. "
                  "Please input an available move.\n")
            display_board = False
            continue
        display_board = True

    print_board(reversi_game)
    print(f"The winner(s) are: {reversi_game.outcome}!")

if __name__ == "__main__":
    start_tui() # pylint: disable=no-value-for-parameter
