"""
CMSC 14200, Spring 2023
Project
Reversi Bot implementation.

People Consulted:
   n/a

Online resources consulted:
   n/a
"""
import random
from abc import ABC, abstractmethod
from typing import Tuple
import click
from reversi import Reversi

class StratBase(ABC):
    '''
    Abstract base class for the Bot strategies
    '''
    _game: Reversi

    def __init__(self, game: Reversi) -> None:
        '''
        Constructor

        Args:
            game [Reversi]: The Reversi game that this player's strategy will be
            used in.
        '''
        self._game = game

    @property
    @abstractmethod
    def best_move(self) -> Tuple[int, int]:
        '''
        Returns the Bot's decision for the best move for the player to make,
        based on the Bot's strategy.
        '''
        raise NotImplementedError

class Random(StratBase):
    '''
    Class for the "Random" Bot strategy, which inherits from "StratBase".
    Chooses a move at random from the available moves.
    '''
    @property
    def best_move(self) -> Tuple[int, int]:
        return random.choice(self._game.available_moves)

class Smart(StratBase):
    '''
    Class for the "Smart" Bot strategy, which inherits from "StratBase".
    Chooses a move by looking one move ahead and determining which of the
        available moves will result in the player having the most pieces on the
        board.
    '''
    @property
    def best_move(self) -> Tuple[int, int]:
        num_pc = self._game.sim_num_pieces(self._game.available_moves, \
                                           self._game.turn)
        best_moves = [key for key, val in num_pc.items() if \
                      val == max(num_pc.values())]
        return random.choice(best_moves)

class VerySmart(StratBase):
    '''
    Class for the "VerySmart" Bot strategy, which inherits from "StratBase".
    Chooses a move by looking two moves ahead and determining which of the
        available moves will result in the highest average number of pieces from
        the second round of available moves. Also will choose a certain move if
        it will cause the player to win the game.
    '''
    @property
    def best_move(self) -> Tuple[int, int]:
        sim_num_pc_avg = {}
        moves = self._game.available_moves
        for move in moves:
            sim = self._game.simulate_moves([move])
            sim_moves = sim.available_moves
            if sim.done and sim.outcome == [sim.turn]:
                return move

            if len(sim_moves) != 0:
                next_num_pc = sim.sim_num_pieces(sim_moves, \
                                                 self._game.turn).values()
                sim_num_pc_avg[move] = sum(next_num_pc) / len(next_num_pc)

        if len(sim_num_pc_avg.keys()) == 0:
            return random.choice(moves)
        best_moves = [key for key, val in sim_num_pc_avg.items() if \
                      val == max(sim_num_pc_avg.values())]
        return random.choice(best_moves)

def play(num_games, player1, player2) -> None:
    '''
    Plays the games.

    Args:
        num_games: number of games to play
        player1: Bot strategy for player 1
        player2: Bot strategy for player 2
    '''
    p1_strat: StratBase
    p2_strat: StratBase

    wins_1 = 0
    wins_2 = 0
    ties = 0

    # play games
    for _ in range(num_games):

        game = Reversi(8, 2, True)

        while not game.done:
            if game.turn == 1:
                if player1 == "random":
                    p1_strat = Random(game)
                elif player1 == "smart":
                    p1_strat = Smart(game)
                else:
                    p1_strat = VerySmart(game)

                if len(game.available_moves) == 0:
                    game.load_game(2, game.grid)
                else:
                    game.apply_move(p1_strat.best_move)

            else:
                if player2 == "random":
                    p2_strat = Random(game)
                elif player2 == "smart":
                    p2_strat = Smart(game)
                else:
                    p2_strat = VerySmart(game)

                if len(game.available_moves) == 0:
                    game.load_game(1, game.grid)
                else:
                    game.apply_move(p2_strat.best_move)

        # assign points
        if len(game.outcome) == 2:
            ties += 1
        elif game.outcome[0] == 1:
            wins_1 += 1
        elif game.outcome[0] == 2:
            wins_2 += 1

    # print win stats
    print(f"Player 1 wins: {wins_1 / num_games * 100:.2f}%")
    print(f"Player 2 wins: {wins_2 / num_games * 100:.2f}%")
    print(f"Ties: {ties / num_games * 100:.2f}%")

bot_strats = ["random", "smart", "very-smart"]
@click.command("bot")
@click.option("-n", "--num-games", default=250)
@click.option("-1", "--player1", type=click.Choice(bot_strats), \
              default="random")
@click.option("-2", "--player2", type=click.Choice(bot_strats), \
              default="random")
def init_game(num_games, player1, player2):
    """
    Initiates a game based on command-line parameters for the number of games of
    Reversi to play and the two bot strategies
    """
    play(int(num_games), player1, player2)

if __name__ == "__main__":
    init_game() # pylint: disable=no-value-for-parameter
