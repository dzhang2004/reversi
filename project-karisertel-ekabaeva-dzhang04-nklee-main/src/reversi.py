"""
Reversi implementation.

Contains a base class (ReversiBase). You must implement
a Reversi class that inherits from this base class.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional
from copy import deepcopy

BoardGridType = List[List[Optional[int]]]
"""
Type for representing the state of the game board (the "grid")
as a list of lists. Each entry will either be an integer (meaning
there is a piece at that location for that player) or None,
meaning there is no piece in that location. Players are
numbered from 1.
"""

ListMovesType = List[Tuple[int, int]]
"""
Type for representing lists of moves on the board.
"""


class ReversiBase(ABC):
    """
    Abstract base class for the game of Reversi
    """

    _side: int
    _players: int
    _othello: bool

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        self._side = side
        self._players = players
        self._othello = othello

    #
    # PROPERTIES
    #

    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players

    @property
    @abstractmethod
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        raise NotImplementedError

    #
    # METHODS
    #

    @abstractmethod
    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        raise NotImplementedError

    @abstractmethod
    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        raise NotImplementedError

    @abstractmethod
    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.

        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.

        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).

        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.

        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)

        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def simulate_moves(self, moves: ListMovesType) -> "ReversiBase":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).

        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.

        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:

        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)

        Args:
            moves: List of positions, representing moves.

        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.

        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        raise NotImplementedError


class Reversi(ReversiBase):
    """
    Class for the game of Reversi, which inherits from "ReversiBase".
    """
    _grid: List[List[Optional[int]]]
    _turn: int

    def __init__(self, side: int, players: int, othello: bool):

        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        super().__init__(side, players, othello)
        self._grid = [[None] * side for _ in range(side)]
        if self._players % 2 != len(self._grid) % 2:
            raise ValueError("Parity of side and players is incorrect")
        if othello and self._players != 2:
            raise ValueError("Othello game can only have 2 players")
        if len(self._grid) < 3:
            raise ValueError("Size of board must be larger than 2 "
                             "cells per side")

        if othello:
            bot_right_center = self._side // 2
            self._grid[bot_right_center][bot_right_center] = 2
            self._grid[bot_right_center - 1][bot_right_center] = 1
            self._grid[bot_right_center - 1][bot_right_center - 1] = 2
            self._grid[bot_right_center][bot_right_center - 1] = 1

        self._turn = 1

    #
    # PROPERTIES
    #

    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players

    @property
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        return self._turn

    def _in_bounds(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a certain position is on the board

        Args:
            pos (tuple[int, int]): the position (row, column)

        Returns:
            bool: if the position is on the board
        """
        row, col = pos
        return 0 <= row < self._side and 0 <= col < self._side

    def _check_direction(self,
                   player: int,
                   pos: Tuple[int, int],
                   direction: Tuple[int, int],
                   ) -> Optional[Tuple[int, int]]:
        """
        Checks if a placed piece has a corresponding origin piece to capture
        along the line connecting the two

        Args:
            player (int): the piece
            pos (tuple[int, int]): the position of the piece
            direction (tuple[int, int]): the direction to check

        Returns:
            Optional[tuple[int, int]]: the position if it exists,
                None if it doesn't
        """
        r_shift, c_shift = direction
        row, col = pos
        check_row = row + r_shift
        check_col = col + c_shift
        if not self._in_bounds((check_row, check_col)):
            return None

        loc_piece = self._grid[check_row][check_col]
        if loc_piece not in (None, player):
            while loc_piece not in (None, player):
                check_row += r_shift
                check_col += c_shift
                if not self._in_bounds((check_row, check_col)):
                    return None
                loc_piece = self._grid[check_row][check_col]

            if self._in_bounds((check_row, check_col)):
                if loc_piece == player:
                    return (check_row, check_col)
        return None

    def _center_pieces(self) -> ListMovesType:
        """
        Finds the list of positions that are considered in the center of the
        board
        
        Returns:
            ListMovesType: the list of positions that are considered the
                center
        """
        center_sq = []
        for i in range((self._side - self._players) // 2,
                       self._side - (self._side - self._players) // 2):
            for j in range((self._side - self._players) // 2,
                           self._side - (self._side - self._players) // 2):
                center_sq.append((i, j))
        return center_sq

    @property
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        moves = set()
        for i, row in enumerate(self._grid):
            for j, _ in enumerate(row):
                if self.legal_move((i, j)):
                    moves.add((i, j))

        return list(moves)

    @property
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        no_moves = True
        current_player = self._turn
        for player in range(1, self._players + 1):
            self._turn = player
            no_moves = no_moves and len(self.available_moves) == 0
        self._turn = current_player
        return no_moves

    @property
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        winner_lst: List[int] = []
        if not self.done:
            return winner_lst

        player_pieces = {}
        for row in self._grid:
            for cell in row:
                if cell is not None:
                    if cell not in player_pieces:
                        player_pieces[cell] = 1
                    else:
                        player_pieces[cell] += 1
        maximum_pieces = 0
        for pieces in player_pieces.values():
            if pieces > maximum_pieces:
                maximum_pieces = pieces
        for player, pieces in player_pieces.items():
            if pieces == maximum_pieces:
                if isinstance(player, int):
                    winner_lst.append(player)
        return winner_lst

    #
    # METHODS
    #

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        if not self._in_bounds(pos):
            raise ValueError("Specified position is outside the bounds of the "
            "board")
        row, col = pos
        return self._grid[row][col]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        if not self._in_bounds(pos):
            raise ValueError("Specified position is outside the bounds of the "
            "board")
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), \
                      (-1, 1), (1, -1), (-1, -1)]
        row, col = pos
        if self._grid[row][col] is not None:
            return False
        center_sqs = self._center_pieces()
        not_filled = None in [self.piece_at(sq) for sq in center_sqs]

        if not_filled:
            for i, iter_row in enumerate(self._grid):
                for j, iter_piece in enumerate(iter_row):
                    if (i, j) not in center_sqs and iter_piece is not None:
                        for direction in directions:
                            move_loc = self._check_direction(self._turn, pos,
                                                             direction)
                            if move_loc is not None:
                                return True
                        return False
            return pos in center_sqs and self._grid[row][col] is None

        for direction in directions:
            move_loc = self._check_direction(self._turn, pos, direction)
            if move_loc is not None:
                return True
        return False

    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.

        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.

        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).

        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """
        if not self._in_bounds(pos):
            raise ValueError("Specified position is outside the bounds of the "
            "board")
        row, col = pos
        if not self._othello and pos in self._center_pieces():
            self._grid[row][col] = self._turn
        else:
            self._grid[row][col] = self._turn
            retrace_dir: List[Tuple[int, int]] = []
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), \
                        (-1, 1), (1, -1), (-1, -1)]
            for direction in directions:
                origin_loc = self._check_direction(self._turn, pos, direction)
                if origin_loc is not None:
                    retrace_dir.append(direction)
            for direction in retrace_dir:
                r_shift, c_shift = direction
                check_row = row + r_shift
                check_col = col + c_shift
                while self._grid[check_row][check_col] != self._turn:
                    self._grid[check_row][check_col] = self._turn
                    check_row += r_shift
                    check_col += c_shift
        self._turn = (self._turn + 1) % (self._players + 1)
        if self._turn == 0:
            self._turn += 1
        while len(self.available_moves) == 0 and not self.done:
            self._turn = (self._turn + 1) % (self._players + 1)
            if self._turn == 0:
                self._turn += 1

    def sim_num_pieces(self, moves: ListMovesType, turn: int) \
                       -> Dict[Tuple[int, int], int]:
        '''
        Simulates several games and gives the number of pieces that the player
        would have on the board if they played each of those moves.

        Args:
            moves: the available moves
            turn: the player whose turn it is

        Returns: A dictionary that maps each move to the number of pieces the
        player would have on the board after playing that move.
        '''
        pieces_dict = {}
        for move in moves:
            sim = self.simulate_moves([move])
            num_pieces = 0
            for i, row in enumerate(sim.grid):
                for j, _ in enumerate(row):
                    if sim.piece_at((i, j)) == turn:
                        num_pieces += 1
            pieces_dict[move] = num_pieces
        return pieces_dict

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.

        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)

        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.

        Returns: None
        """
        if turn <= 0 or turn > self._players:
            raise ValueError("Value of turn is inconsistent with the number of "
                             "players")
        if len(grid) != len(self._grid):
            raise ValueError("Length of inputted grid is inconsistent with "
                             "current grid size")
        for _, row in enumerate(grid):
            for _, item in enumerate(row):
                if item is not None:
                    if item <= 0 or item > self._players:
                        raise ValueError("Value of turn is inconsistent with "
                                     "the number of players")

        self._turn = turn
        self._grid = grid

    def simulate_moves(self, moves: ListMovesType) -> "Reversi":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).

        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.

        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:

        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)

        Args:
            moves: List of positions, representing moves.

        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.

        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        sim_reversi = Reversi(self._side, self._players, self._othello)
        sim_reversi.load_game(self._turn, self.grid)
        for move in moves:
            row, col = move
            if not self._in_bounds(move):
                raise ValueError("Specified position is outside the bounds of"
                 "the board")
            if sim_reversi.grid[row][col] is not None:
                raise ValueError("There is already a piece at this location")
            sim_reversi.apply_move(move)
        return sim_reversi


class Piece:
    """
    Class for a piece in a board game
    """

    _pos: Tuple[int, int]
    _grid: List[List[Optional[int]]]

    def __init__(self, side: int, players: int, othello: bool,
                 pos: Tuple[int, int]):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.
            pos: position of piece

        Raises:
            ValueError: If the position is outside the bounds of the board
        """
        self._pos = pos

        reversi_game = Reversi(side, players, othello)
        self._grid = reversi_game._grid

        if not reversi_game._in_bounds(self._pos):
            raise ValueError("Specified position is outside the bounds of"
                "the board")

    @property
    def player_num(self) -> Optional[int]:
        """
        Returns the player the piece belongs to

        Args:
            None other than self

        Returns: The number of the player (players are numbered from 1).
        """
        row, col = self._pos
        return self._grid[row][col]

    @property
    def piece_at(self) -> Tuple[int, int]:
        """
        Returns the position of the piece

        Args:
            None other than self

        Returns: Returns the position of the piece
        """
        return self._pos

class Board:
    """
    Class for a game-agnostic board.
    """
    _grid: List[List[Optional[Piece]]]
    _side: int
    _players: int
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int) -> None:
        self._side = side
        self._grid = [[None] * side for _ in range(side)]
        self._players = players
        self._turn = 1
        self._num_moves = 0

    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players

    @property
    def grid(self) -> List[List[Optional[Piece]]]:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        return self._turn

    def _in_bounds(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a certain position is on the board

        Args:
            pos (tuple[int, int]): the position (row, column)

        Returns:
            bool: if the position is on the board
        """
        row, col = pos
        return 0 <= row < self._side and 0 <= col < self._side
