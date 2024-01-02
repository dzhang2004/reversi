"""
Mock implementations of ReversiBase.

We provide a ReversiStub implementation, and you must
implement a ReversiMock implementation.
"""
from typing import List, Tuple, Optional
from copy import deepcopy

from reversi import ReversiBase, BoardGridType, ListMovesType


class ReversiStub(ReversiBase):
    """
    Stub implementation of ReversiBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players and boards of size 2x2 and above.
    - The board is always initialized with four pieces in the four corners
      of the board. Player 1 has pieces in the northeast and southwest
      corners of the board, and Player 2 has pieces in the southeast and
      northwest corners of the board.
    - All moves are legal, even if there is already a piece in a given position.
    - The game ends after four moves. Whatever player has a piece in position
      (0,1) wins. If there is no piece in that position, the game ends in a tie.
    - It does not validate board positions. If a method
      is called with a position outside the board, the method will likely cause
      an exception.
    - It does not implement the ``load_game`` or ``simulate_moves`` method.
    """

    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, othello: bool):
        if players != 2:
            raise ValueError("The stub implementation "
                             "only supports two players")

        super().__init__(side, players, othello)

        self._grid = [[None]*side for _ in range(side)]
        self._grid[0][-1] = 1
        self._grid[-1][0] = 1
        self._grid[0][0] = 2
        self._grid[-1][-1] = 2

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        return self._num_moves == 4

    @property
    def outcome(self) -> List[int]:
        if not self.done:
            return []

        if self._grid[0][1] is None:
            return [1, 2]
        else:
            return [self._grid[0][1]]

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        row, col = pos
        return self._grid[row][col]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        return True

    def apply_move(self, pos: Tuple[int, int]) -> None:
        row, col = pos
        self._grid[row][col] = self._turn
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        raise NotImplementedError()

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> ReversiBase:
        raise NotImplementedError()


class ReversiMock(ReversiBase):
    """
    Mock implementation of ReversiBase.

    This mock implementation behaves according to the following rules:

    - It only supports two players and boards of size 4x4 and above.
    - Validates the parity of the board size (that the side of the board has an
      even size)
    - Supports the optional othello parameter
    - Raises ValueError as specified in ReversiBase
    - A move is legal if the position in the board is empty, and there is at
      least one piece (of any player) in an adjacent square (in any direction,
      including diagonals). Placing a piece in position (0, 0) or (side-1,
      side-1) is always legal.
    - If a player places a piece in position (0, 0), they win and the game ends.
    - If a player places a piece in position (side-1, side-1), the game ends,
      and both players win the game (i.e., the game ends in a tie).
    - It does not implement the ``load_game`` method.
    - It supports simulating a single move in ``simulate_moves``.
    """

    _side: int
    _players: int
    _othello: bool
    _grid: BoardGridType
    _turn: int
    _num_moves: int
    # _location_of_pieces: Dict[int, List[Tuple(int, int)]]

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Notes:
            - side must be even, any 4x4+ size board
            - only two players for this implementation

        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        super().__init__(side, players, othello)
        if players != 2:
            raise ValueError("The mock implementation "
                             "only supports two players")
        if side < 4:
            raise ValueError("The mock implementation only "
                             "supports boards of size 4x4 or larger")
        if side % 2 != players % 2:
            raise ValueError("The parities of the number of squares "
                             "and number of players does not match")
        self._grid = [[None] * side for _ in range(side)]

        if othello:
            bot_right_center = self._side // 2
            self._grid[bot_right_center][bot_right_center] = 2
            self._grid[bot_right_center - 1][bot_right_center] = 1
            self._grid[bot_right_center - 1][bot_right_center - 1] = 2
            self._grid[bot_right_center][bot_right_center - 1] = 1

        self._turn = 1
        self._num_moves = 0

    #
    # PROPERTIES
    #

    @property
    def size(self) -> int:
        return self._side

    @property
    def num_players(self) -> int:
        return self._players

    @property
    def grid(self) -> BoardGridType:
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
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

    @property
    def available_moves(self) -> ListMovesType:
        moves = set()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), \
                      (-1, 1), (1, -1), (-1, -1)]

        for r_i, row in enumerate(self.grid):
            for col, piece in enumerate(row):
                if piece is not None:
                    for direction in directions:
                        r_direction, c_direction = direction
                        if 0 <= r_i + r_direction < len(self.grid) and \
                                0 <= col + c_direction < len(self.grid[0]):
                            if self.grid[r_i + r_direction][col + c_direction] \
                                    is None:
                                moves.add((r_i + r_direction, \
                                           col + c_direction))

        moves.add((0, 0))
        moves.add((self._side - 1, self._side - 1))
        return list(moves)


    @property
    def done(self) -> bool:
        if self._grid[0][0] is not None:
            return True
        if self._grid[self._side - 1][self._side - 1] is not None:
            return True

        return False

    @property
    def outcome(self) -> List[int]:
        if self._grid[0][0] is not None:
            return [self._grid[0][0]]
        elif self._grid[self._side - 1][self._side - 1] is not None:
            return [1, 2]
        else:
            return []


    #
    # METHODS
    #

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.
        """
        if not self._in_bounds(pos):
            raise ValueError("Specified position is outside the bounds of the "
            "board")
        row, col = pos
        return self._grid[row][col]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.
        """
        if not self._in_bounds(pos):
            raise ValueError("Specified position is outside the bounds of the "
            "board")
        return pos in self.available_moves

    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.
        """
        if not self.legal_move(pos):
            raise ValueError("Specified position is outside the bounds of the "
            "board")
        i, k = pos
        self._grid[i][k] = self._turn
        new_player = (self._turn + 1) % (self._players + 1)
        if new_player == 0:
            new_player += 1
        self._turn = new_player


    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        This mock implementation does not implement the ``load_game`` method.
        """
        raise NotImplementedError

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
        """
        This mock implementation support simulating a single move.

        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.
        """
        sim_reversi = ReversiMock(self._side, self._players, self._othello)
        for move in moves:
            if not self.legal_move(move):
                raise ValueError("One or more positions is outside the bounds "
                                 "of the board")
            sim_reversi.apply_move(move)
        return sim_reversi


class ReversiBotMock(ReversiMock):
    '''
    Version of the ReversiMock class used in the Bot mock implementation.
    '''
    @property
    def available_moves(self) -> ListMovesType:
        moves = set()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), \
                      (-1, 1), (1, -1), (-1, -1)]

        for row_i, row in enumerate(self._grid):
            for col, piece in enumerate(row):
                if piece is not None:
                    for direction in directions:
                        r_direction, c_direction = direction
                        if self._in_bounds((row_i + r_direction, \
                                            col + c_direction)) and \
                           self._grid[row_i + r_direction][col + c_direction] \
                           is None:
                            moves.add((row_i + r_direction, col + c_direction))

        if len(moves) == 0:
            self._turn = 2 if self._turn == 1 else 1
        return list(moves)

    @property
    def done(self) -> bool:
        '''
        Returns True if the game is over, False otherwise. The game is
        considered over if all of the spots in the board are full.
        '''
        for row in self._grid:
            for piece in row:
                if piece is None:
                    return False
        return True

    @property
    def outcome(self) -> List[int]:
        num_pieces = [0 for x in range(self.num_players)]
        for row_i, row in enumerate(self._grid):
            for col_i, _ in enumerate(row):
                player = self.piece_at((row_i, col_i))
                if player is not None:
                    num_pieces[player - 1] += 1

        winning_score = num_pieces[0]
        winners = []
        for i, num in enumerate(num_pieces):
            if num > winning_score:
                winning_score = num
                winners = [i + 1]
            elif num == winning_score:
                winners.append(i + 1)

        return winners

    def apply_move(self, pos: Tuple[int, int]) -> None:
        '''
        Any pieces belonging to other players in those squares will be converted
        to pieces of the player making a move.
        '''
        if not self.legal_move(pos):
            raise ValueError("Specified position is outside the bounds of the "
            "board")
        i, k = pos
        self._grid[i][k] = self._turn
        adj_sq = [(i - 1, k - 1), (i - 1, k), (i - 1, k + 1), \
                  (i, k - 1), (i, k + 1), \
                  (i + 1, k - 1), (i + 1, k), (i + 1, k + 1)]
        for square in [rc for rc in adj_sq if self._in_bounds(rc)]:
            if self.piece_at((square[0], square[1])) not in [None, self._turn]:
                self._grid[square[0]][square[1]] = self._turn

        new_player = (self._turn + 1) % (self._players + 1)
        if new_player == 0:
            new_player += 1
        self._turn = new_player

    def load_game(self, turn: int, grid: BoardGridType) -> None:
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
                        raise \
                            ValueError("Value of turn is inconsistent with the "
                                     "number of players")

        self._turn = turn
        self._grid = grid

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBotMock":
        sim_reversi = ReversiBotMock(self._side, self._players, self._othello)
        sim_reversi.load_game(2, self._grid) # loading game
        self._turn = 2
        for move in moves:
            if not sim_reversi.legal_move(move):
                raise ValueError("One or more positions is outside the bounds "
                                 "of the board")
            sim_reversi.apply_move(move)
        return sim_reversi
