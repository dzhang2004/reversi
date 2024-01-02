"""
Tests for the game of Reversi
"""

from typing import List, Tuple, Set, Optional
import pytest
from reversi import Reversi

def helper_construct_even(side: int, players: int, othello: bool) -> None:
    """
    Test whether the Reversi game constructor works properly.
    We assume just two players. Helper function for cases, when size length is 
    even and in range.

    Arguments:
        side[int]: the side of the board
        players[int]: the number of players
        othello[bool]: True if it is an othello game, False otherwise
    """
    reversi = Reversi(side, players, othello)
    assert len(reversi.grid) >= 3
    assert len(reversi.grid) == side
    for i, row in enumerate(reversi.grid):
        assert len(row) == side
        for k, val in enumerate(row):
            assert val is None, f"Expected grid[{i}][{k}] to be None not {val}"
    assert not reversi.done
    assert reversi.outcome == []
    assert reversi.turn == 1

def helper_legal(reversi: "Reversi", legal: Set[Tuple[int, int]]) -> None:
    """
    Tests if the given set for a given board is mapping the legal_moves output.

    Arguments:
        reversi[Reversi]: the object Reversi - the board created with given 
        parameters
        legal[Set[Tuple[int, int]]]: the list of legal moves to fill the 
        center of the board
    """
    for i in range(reversi.size):
        for k in range(reversi.size):
            if (i, k) in legal:
                assert reversi.legal_move(
                    (i, k)
                ), f"{(i,k)} is a legal move, but legal_move returned False"
            else:
                assert not reversi.legal_move(
                    (i, k)
                ), f"{(i, k)} is not a legal move, but legal_move returned True"

def test_construct_board1():
    """
    Test whether the Reversi game constructor works properly.
    We assume just two players. Side = 4
    """
    helper_construct_even(side=4, players=2, othello=False)

def test_construct_board2():
    """
    Test whether the Reversi game constructor works properly.
    We assume just two players. Side = 6
    """
    helper_construct_even(side=6, players=2, othello=False)

def test_construct_board3():
    """
    Test whether the Reversi game constructor works properly.
    We assume just two players. Side = 8
    """
    helper_construct_even(side=8, players=2, othello=False)

def test_construct_board4():
    """
    Test whether the Reversi game constructor works properly.
    We assume just two players. Side = 5.
    """
    with pytest.raises(ValueError):
        Reversi(side=5, players=2, othello=False)

def test_construct_board5():
    """
    Test whether the Reversi game constructor works properly.
    We assume just two players. Side = 7.
    """
    with pytest.raises(ValueError):
        Reversi(side=7, players=2, othello=False)

def test_construct_board6():
    """
    Test whether the Reversi game constructor works properly.
    We assume just two players. Side = 2.
    """
    with pytest.raises(ValueError):
        Reversi(side=2, players=2, othello=False)

def test_construct_othello1():
    """
    Test whether the Othello game constructor works properly for 8x8 board.
    We assume just two players.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    assert len(reversi.grid) == 8
    othello_pos = [(3, 3, 2), (3, 4, 1), (4, 3, 1), (4, 4, 2)]

    for i, row in enumerate(reversi.grid):
        assert len(row) == 8
        for k, val in enumerate(row):
            if i in (3, 4) and k in (3, 4):
                continue
            assert val is None, f"Expected grid[{i}][{k}] to be None not {val}"

    for i, k, player in othello_pos:
        assert (
            reversi.grid[i][k] == player
        ), f"Expected grid[{i}][{k}] to be {player} not {reversi.grid[i][k]}"

    assert not reversi.done
    assert reversi.outcome == []
    assert reversi.turn == 1

def test_construct_othello2():
    """
    Test whether the Othello game constructor works properly for 20x20 board.
    We assume just two players.
    """
    reversi = Reversi(side=20, players=2, othello=True)
    assert len(reversi.grid) == 20
    othello_pos = [(9, 9, 2), (9, 10, 1), (10, 9, 1), (10, 10, 2)]

    for i, row in enumerate(reversi.grid):
        assert len(row) == 20
        for k, val in enumerate(row):
            if i in (9, 10) and k in (9, 10):
                continue
            assert val is None, f"Expected grid[{i}][{k}] to be None not {val}"
    for i, k, player in othello_pos:
        assert (
            reversi.grid[i][k] == player
        ), f"Expected grid[{i}][{k}] to be {player} not {reversi.grid[i][k]}"

    assert not reversi.done
    assert reversi.outcome == []
    assert reversi.turn == 1

def test_construct_othello3():
    """
    Test whether the Othello game constructor works properly for 2x2 board.
    We assume just two players.
    """
    with pytest.raises(ValueError):
        Reversi(side=2, players=2, othello=True)

def test_construct_othello4():
    """
    Test whether the Othello game constructor works properly for 5x5 board.
    We assume just two players.
    """
    with pytest.raises(ValueError):
        Reversi(side=5, players=2, othello=True)

def test_othello_8_size():
    """
    Test whether the Othello game constructor works properly for size propety.
    Side = 8.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    assert len(reversi.grid) == 8
    for elements in reversi.grid:
        assert len(elements) == 8

def test_othello_8_players1():
    """
    Test whether the Othello game constructor works properly for the players
    propety. Side = 8.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    assert reversi.num_players == 2

def test_othello_8_players2():
    """
    Test whether the Othello game constructor works properly for the players
    propety. Side = 8.
    """
    with pytest.raises(ValueError):
        Reversi(side=8, players=4, othello=True)

def test_othello_8_players3():
    """
    Test whether the Othello game constructor works properly for the players
    propety. Side = 8. It should not store anything since the size is incorrect.
    """
    with pytest.raises(ValueError):
        Reversi(side=8, players=3, othello=True)

def test_othello_8_turn1():
    """
    Test whether the Othello game constructor works properly for the turn
    propety. Side = 8.
    """
    reversi = Reversi(side=8, players = 2, othello=True)
    assert reversi.turn == 1

def test_othello_8_turn2():
    """
    Test whether the Othello game constructor works properly for the turn
    propety. Side = 8.
    """
    reversi = Reversi(side=8, players = 2, othello=True)
    reversi.apply_move((2, 3))
    assert reversi.turn == 2

def test_othello_8_piece_at1():
    """
    Test whether the Othello game constructor works properly for the piece_at
    method. Side = 8.
    """
    reversi = Reversi(side=8, players = 2, othello=True)
    assert reversi.piece_at((3, 3)) == 2
    assert reversi.piece_at((3, 4)) == 1
    assert reversi.piece_at((4, 3)) == 1
    assert reversi.piece_at((4, 4)) == 2

def test_othello_8_piece_at2():
    """
    Test whether the Othello game constructor works properly for the piece_at
    method. Side = 8.
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players = 2, othello=True)
        reversi.piece_at((-1, -1))
    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players = 2, othello=True)
        reversi.piece_at((8, 8))

def test_othello_8_legal_move1():
    """
    Test whether the Othello game constructor works properly for the legal move
    method. Side = 8.
    """
    reversi = Reversi(side=8, players = 2, othello=True)
    legal = {(2,3), (3,2), (4,5), (5,4)}

    helper_legal(reversi, legal)

def test_othello_8_legal_move2():
    """
    Test whether the Othello game constructor works properly for the legal move
    method. Side = 8.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    with pytest.raises(ValueError):
        reversi.piece_at((-1, -1))
    with pytest.raises(ValueError):
        reversi.piece_at((8, 8))

def test_othello_8_available_moves():
    """
    Test whether the Othello game constructor works properly for the
    available moves method. Side = 8.
    """
    reversi = Reversi(side=8, players = 2, othello=True)
    expected = {(2,3), (3,2), (4,5), (5,4)}
    assert set(reversi.available_moves) == expected

def test_othello_8_apply_move1():
    """
    Test whether the Othello game apply_move method. Constructor uses size 8.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    reversi.apply_move((4, 5))
    assert reversi.piece_at((4, 5)) == 1
    assert reversi.turn == 2
    assert not reversi.done
    assert reversi.outcome == []

def test_othello_8_apply_move2():
    """
    Test whether the Othello game apply_move method. Constructor uses size 8.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    assert reversi.turn == 1
    reversi.apply_move((4, 5))
    assert reversi.turn == 2
    reversi.apply_move((5, 5))
    assert reversi.turn == 1
    assert reversi.piece_at((4, 5)) == 1
    assert reversi.piece_at((5, 5)) == 2
    assert not reversi.done
    assert reversi.outcome == []

def test_othello_8_apply_move3():
    """
    Test whether the Othello game apply_move method. Constructor uses size 8.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    assert reversi.turn == 1
    reversi.apply_move((4, 5))
    assert reversi.turn == 2
    reversi.apply_move((5, 5))
    assert reversi.turn == 1
    reversi.apply_move((5, 4))
    assert reversi.turn == 2
    assert reversi.piece_at((4, 5)) == 1
    assert reversi.piece_at((5, 5)) == 2
    assert reversi.piece_at((5, 4)) == 1
    assert not reversi.done
    assert reversi.outcome == []

def test_othello_8_apply_move4():
    """
    Test whether the Othello game apply_move method. Constructor uses size 8.
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.apply_move((-1, -1))
    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.apply_move((8, 8))

def helper_othello_4_end(end_game: List[Tuple[int, int]]) -> "Reversi":
    """
    Helper function to test whether the Othello game has right values after 
    the end of the game. Constructor uses size 4.
    
    Arguments[List[Tuple[int, int]]]: the list of moves which will result in the
    end of the game.
    """
    reversi = Reversi(side=4, players=2, othello=True)
    for move in end_game:
        i, k = move
        reversi.apply_move(move)
        assert reversi.grid[i][k] is not None
    return reversi

def test_othello_4_end1():
    """
    Test whether the Othello game has right values after the end of the game. 
    Constructor uses size 4. Player 1 wins.
    """
    end_game = [(3, 2), (3, 1), (1, 0), (0, 1), (3, 0), (2, 3), (1, 3), (2, 0),\
                (3, 3), (0, 3), (0, 2), (0, 0)]
    final = helper_othello_4_end(end_game)
    assert final.done
    assert final.outcome == [1]

def test_othello_4_end2():
    """
    Test whether the Othello game has right values after the end of the game. 
    Constructor uses size 4. Player 2 wins.
    """
    end_game = [(0, 1), (0, 0), (1, 0), (2, 0), (3, 2), (0, 2), (3, 0), (2, 3),\
                (0, 3), (3, 1), (3, 3), (1, 3)]
    final = helper_othello_4_end(end_game)
    assert final.done
    assert final.outcome == [2]

def test_othello_4_end3():
    """
    Test whether the Othello game has right values after the end of the game. 
    Constructor uses size 4. Obtains tie.
    """
    end_game = [(2, 3), (3, 1), (3, 0), (3, 3), (3, 2), (1, 3), (0, 3), (0, 1),\
                (0, 0), (2, 0), (0, 2), (1, 0)]
    final = helper_othello_4_end(end_game)
    assert final.done
    assert final.outcome == [1, 2]

def test_othello_6_1():
    """
    Test whether the Othello game constructor works properly for 6x6 board.
    We assume just two players.Testing for num_players
    """
    reversi = Reversi(side=6, players=2, othello=True)
    assert reversi.num_players == 2

def test_othello_6_2():
    """
    Test whether the Othello game constructor works properly for 6x6 board.
    We assume just two players. Testing for side
    """
    reversi = Reversi(side=6, players=2, othello=True)
    assert reversi.size == 6

def test_othello_6_3():
    """
    Test whether the Othello game constructor works properly for 6x6 board.
    We assume just two players. Testing for turn
    """
    reversi = Reversi(side=6, players=2, othello=True)
    assert reversi.turn == 1
    reversi.apply_move((1, 2))
    assert reversi.turn == 2
    reversi.apply_move((3, 1))
    assert reversi.turn == 1

def test_othello_6_4():
    """
    Test whether the Othello game constructor works properly for 6x6 board.
    We assume just two players. Testing for piece_at
    """
    reversi = Reversi(side=6, players=2, othello=True)
    assert reversi.piece_at((2, 2)) == 2
    assert reversi.piece_at((2, 3)) == 1
    assert reversi.piece_at((3, 3)) == 2
    reversi.apply_move((1, 2))
    assert reversi.piece_at((1, 2)) == 1
    reversi.apply_move((3, 1))
    assert reversi.piece_at((3, 1)) == 2
    with pytest.raises(ValueError):
        reversi.piece_at((6, 6))
    with pytest.raises(ValueError):
        reversi.piece_at((-1, 0))

def test_othello_6_5():
    """
    Test whether the Othello game constructor works properly for 6x6 board.
    We assume just two players. Testing for available_moves
    """
    reversi = Reversi(side=6, players=2, othello=True)
    expected = {(1, 2), (2, 1), (3, 4), (4, 3)}
    assert set(reversi.available_moves) == expected
    reversi.apply_move((1, 2))
    expected_new = {(1, 3), (3, 1), (1, 1)}
    assert set(reversi.available_moves) == expected_new

def test_othello_6_6():
    """
    Test whether the Othello game constructor works properly for 6x6 board.
    We assume just two players. Testing for legal_move
    """
    reversi = Reversi(side=6, players=2, othello=True)
    legal = {(1, 2), (2, 1), (3, 4), (4, 3)}
    helper_legal(reversi, legal)

def test_othello_20_1():
    """
    Test whether the Othello game constructor works properly for 20x20 board.
    We assume just two players. Testing for num_players.
    """
    reversi = Reversi(side=20, players=2, othello=True)
    assert reversi.num_players == 2

def test_othello_20_2():
    """
    Test whether the Othello game constructor works properly for 20x20 board.
    We assume just two players. Testing for side.
    """
    reversi = Reversi(side=20, players=2, othello=True)
    assert reversi.size == 20

def test_othello_20_3():
    """
    Test whether the Othello game constructor works properly for 20x20 board.
    We assume just two players. Testing for turn.
    """
    reversi = Reversi(side=20, players=2, othello=True)
    assert reversi.turn == 1
    reversi.apply_move((8, 9))
    assert reversi.turn == 2
    reversi.apply_move((10, 8))
    assert reversi.turn == 1

def test_othello_20_4():
    """
    Test whether the Othello game constructor works properly for 20x20 board.
    We assume just two players. Testing for piece_at.
    """
    reversi = Reversi(side=20, players=2, othello=True)
    assertion_lst = [(9, 9), (10, 10), (9, 10), (10, 9)]
    for element in assertion_lst[:2]:
        assert reversi.piece_at(element) == 2
    for element in assertion_lst[2:]:
        assert reversi.piece_at(element) == 1
    reversi.apply_move((8, 9))
    assert reversi.piece_at((8, 9)) == 1
    reversi.apply_move((10, 8))
    assert reversi.piece_at((10, 8)) == 2
    with pytest.raises(ValueError):
        reversi.piece_at((20, 19))
    with pytest.raises(ValueError):
        reversi.piece_at((-1, 1))

def test_othello_20_5():
    """
    Test whether the Othello game constructor works properly for 20x20 board.
    We assume just two players. Testing for available_moves.
    """
    reversi = Reversi(side=20, players=2, othello=True)
    expected = {(8, 9), (9, 8), (10, 11), (11, 10)}
    assert set(reversi.available_moves) == expected
    reversi.apply_move((8, 9))
    expected_new = {(8, 10), (10, 8), (8, 8)}
    assert set(reversi.available_moves) == expected_new

def test_othello_20_6():
    """
    Test whether the Othello game constructor works properly for 20x20 board.
    We assume just two players. Testing for available_moves.
    """
    reversi = Reversi(side=20, players=2, othello=True)
    legal = {(8, 9), (9, 8), (10, 11), (11, 10)}
    helper_legal(reversi, legal)

def test_non_othello_8a_1():
    """
    Tests an 8x8 non-Othello two player game: verify that available_moves 
    will only allow moves in the center square.
    """
    reversi = Reversi(side=8, players=2, othello=False)
    available = {(3, 3), (3, 4), (4, 3), (4, 4)}
    assert set(reversi.available_moves) == available

def test_non_othello_8l_1():
    """
    Tests an 8x8 non-Othello two player game: verify that legal_move 
    will only allow moves in the center square.
    """
    reversi = Reversi(side=8, players=2, othello=False)
    legal = {(3, 3), (3, 4), (4, 3), (4, 4)}
    helper_legal(reversi, legal)

def test_non_othello_8a_2():
    """
    Tests an 8x8 non-Othello two player game: verify that
    available_moves return results consistent with the center square 
    having been filled in.
    """
    reversi = Reversi(side=8, players=2, othello=False)
    filled_center = [[None for _ in range(8)], [None for _ in range(8)],
            [None for _ in range(8)], [None, None, None,1, 2, None, None, None],
            [None, None, None, 2, 1, None, None, None],[None for _ in range(8)],
            [None for _ in range(8)],[None for _ in range(8)]]
    reversi.load_game(1, filled_center)
    available = {(2, 4), (3, 5), (4, 2), (5, 3)}
    assert set(reversi.available_moves) == available

def test_non_othello_8l_2():
    """
    Tests an 8x8 non-Othello two player game: verify that legal_move returns 
    results consistent with the center square having been filled in.
    """
    reversi = Reversi(side=8, players=2, othello=False)
    filled_center = [[None for _ in range(8)], [None for _ in range(8)],
            [None for _ in range(8)], [None, None, None,1, 2, None, None, None],
            [None, None, None, 2, 1, None, None, None],[None for _ in range(8)],
            [None for _ in range(8)],[None for _ in range(8)]]
    reversi.load_game(1, filled_center)
    legal = {(2, 4), (3, 5), (4, 2), (5, 3)}
    helper_legal(reversi, legal)

def test_non_othello_8a_3():
    """
    Tests an 8x8 non-Othello two player game: verify that
    available_moves returns results consistent with the center square 
    having been filled in.
    """
    reversi = Reversi(side=8, players=2, othello=False)
    filled_center = [[None for _ in range(8)], [None for _ in range(8)],
            [None for _ in range(8)], [None, None, None,1, 1, None, None, None],
            [None, None, None, 2, 2, None, None, None],[None for _ in range(8)],
            [None for _ in range(8)],[None for _ in range(8)]]
    reversi.load_game(1, filled_center)
    available = {(5, 2), (5, 3), (5, 4), (5, 5)}
    assert set(reversi.available_moves) == available

def test_non_othello_8l_3():
    """
    Tests an 8x8 non-Othello two player game: verify that legal_move returns 
    results consistent with the center square having been filled in.
    """
    reversi = Reversi(side=8, players=2, othello=False)
    filled_center = [[None for _ in range(8)], [None for _ in range(8)],
            [None for _ in range(8)], [None, None, None,1, 1, None, None, None],
            [None, None, None, 2, 2, None, None, None],[None for _ in range(8)],
            [None for _ in range(8)],[None for _ in range(8)]]
    reversi.load_game(1, filled_center)
    legal = {(5, 2), (5, 3), (5, 4), (5, 5)}
    helper_legal(reversi, legal)

def test_non_othello_9l_1():
    """
    Tests an 9x9 non-Othello three player game: verify that legal_move 
    will only allow moves in the center square.
    """
    reversi = Reversi(side=9, players=3, othello=False)
    legal = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5),
                (5, 3), (5, 4), (5, 5)}
    helper_legal(reversi, legal)

def test_non_othello_9a_1():
    """
    Tests an 9x9 non-Othello three player game: verify that available_moves will
    only allow moves in the center square.
    """
    reversi = Reversi(side=9, players=3, othello=False)
    available = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5),
                (5, 3), (5, 4), (5, 5)}
    assert set(reversi.available_moves) == available

def test_non_othello_9a_2():
    """
    Tests an 9x9 non-Othello three player game: verify that
    available_moves returns results consistent with the center square 
    having been filled in.
    """
    reversi = Reversi(side=9, players=3, othello=False)
    filled_center = [[None for _ in range(9)], [None for _ in range(9)],
            [None for _ in range(9)],
            [None, None, None, 1, 2, 3, None, None, None],
            [None, None, None, 1, 2, 3, None, None, None],
            [None, None, None, 1, 2, 3, None, None, None],
            [None for _ in range(9)],
            [None for _ in range(9)],[None for _ in range(9)]]
    reversi.load_game(1, filled_center)
    available = {(2, 6), (2, 5), (4, 6), (5, 6), (6, 6), (3, 6), (6, 5)}
    assert set(reversi.available_moves) == available

def test_non_othello_9l_2():
    """
    Tests an 9x9 non-Othello three player game: verify that legal_move returns 
    results consistent with the center square having been filled in.
    """
    reversi = Reversi(side=9, players=3, othello=False)
    filled_center = [[None for _ in range(9)], [None for _ in range(9)],
            [None for _ in range(9)],
            [None, None, None, 1, 2, 3, None, None, None],
            [None, None, None, 1, 2, 3, None, None, None],
            [None, None, None, 1, 2, 3, None, None, None],
            [None for _ in range(9)],
            [None for _ in range(9)],[None for _ in range(9)]]
    reversi.load_game(1, filled_center)
    legal = {(2, 6), (2, 5), (4, 6), (5, 6), (6, 6), (3, 6), (6, 5)}
    helper_legal(reversi, legal)

def test_non_othello_9a_3():
    """
    Tests an 8x8 non-Othello three player game: verify that 
    available_moves returns results consistent with the center square 
    having been filled in.
    """
    reversi = Reversi(side=9, players=3, othello=False)
    filled_center = [[None for _ in range(9)], [None for _ in range(9)],
            [None for _ in range(9)],
            [None, None, None, 2, 3, 3, None, None, None],
            [None, None, None, 1, 1, 2, None, None, None],
            [None, None, None, 3, 2, 1, None, None, None],
            [None for _ in range(9)],
            [None for _ in range(9)],[None for _ in range(9)]]
    reversi.load_game(1, filled_center)
    available = {(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (5, 2), (6, 2), (6, 3),
                    (6, 4), (4, 6), (6, 5)}
    assert set(reversi.available_moves) == available

def test_non_othello_9l_3():
    """
    Tests an 8x8 non-Othello three player game: verify that legal_move returns 
    results consistent with the center square having been filled in.
    """
    reversi = Reversi(side=9, players=3, othello=False)
    filled_center = [[None for _ in range(9)], [None for _ in range(9)],
            [None for _ in range(9)],
            [None, None, None, 2, 3, 3, None, None, None],
            [None, None, None, 1, 1, 2, None, None, None],
            [None, None, None, 3, 2, 1, None, None, None],
            [None for _ in range(9)],
            [None for _ in range(9)],[None for _ in range(9)]]
    reversi.load_game(1, filled_center)
    legal = {(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (5, 2), (6, 2), (6, 3),
                    (6, 4), (4, 6), (6, 5)}
    helper_legal(reversi, legal)

def helper_grid(reversi: "Reversi", grid: List[List[Optional[int]]]) -> None:
    """
    Checks if the actual grid of tests matches the final grid which we got after
    apply_moves.

    Arguments:
        reversi[Reversi]: the object Reversi - the board created with given 
        parameters
        grid: List[List[Optional[int]]]: grid of players which have to be
        after the end of the game
    """
    assert len(reversi.grid) == len(grid)
    for i, _ in enumerate(reversi.grid):
        assert len(reversi.grid[i]) == len(grid[i])
    for i, row in enumerate(reversi.grid):
        for j, col in enumerate(row):
            assert col == grid[i][j]

def test_non_othello_5_1():
    """
    Tests an 5x5 non-Othello three player game: we call apply_move enough times 
    to result in the game ending and then verify that the grid contains the 
    expected pieces, and that done and outcome return values consistent 
    with a game that has ended.
    """
    reversi = Reversi(side=5, players=3, othello=False)
    filled_center = [[None for _ in range(5)], [None, 1, 2, 3, None],
                    [None, 1, 2, 3, None], [None, 1, 2, 3, None],
                    [None for _ in range(5)]]
    reversi.load_game(1, filled_center)
    sequence = [(4, 4), (1, 0), (4, 0), (0, 0), (3, 4), (4, 3), (2, 4), (1, 4),
                (0, 3), (0, 4), (0, 1), (3, 0), (0, 2), (4, 1), (2, 0), (4, 2)]
    for moves in sequence:
        reversi.apply_move(moves)
    assert reversi.outcome == [1]
    assert reversi.done
    grid = [[1, 1, 1, 1, 1], [2, 2, 1, 1, 1], [3, 3, 1, 3, 1], [3, 2, 1, 1, 1],
            [3, 2, 1, 1, 1]]
    helper_grid(reversi, grid)

def test_non_othello_5_2():
    """
    Tests an 5x5 non-Othello three player game: we call apply_move enough times 
    to result in the game ending and then verify that the grid contains the 
    expected pieces, and that done and outcome return values consistent 
    with a game that has ended.
    """
    reversi = Reversi(side=5, players=3, othello=False)
    filled_center = [[None for _ in range(5)], [None, 2, 3, 3, None],
                    [None, 1, 1, 2, None], [None, 3, 2, 1, None],
                    [None for _ in range(5)]]
    reversi.load_game(1, filled_center)
    sequence = [(0, 1), (0, 2), (3, 4), (0, 3), (0, 0), (1, 0), (2, 0), (0, 4),
                (2, 4), (1, 4), (4, 0), (3, 0), (4, 2), (4, 4), (4, 3), (4, 1)]
    for moves in sequence:
        print(reversi.turn)
        reversi.apply_move(moves)
    assert reversi.outcome == [2]
    assert reversi.done
    grid = [[2, 2, 2, 2, 2], [3, 2, 1, 2, 2], [3, 2, 2, 2, 2], [3, 2, 2, 3, 2],
                [2, 2, 2, 2, 2]]
    helper_grid(reversi, grid)

def test_othello_load_8_1():
    """
    Tests an 8x8 Othello board: uses load_game to load a grid with at least five 
    pieces on it and verify that the state of the game was updated correctly.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    grid = [[None for _ in range(8)], [None for _ in range(8)],
            [None for _ in range(8)], [None, None, 1, 1, 1, None, None, None],
            [None, None, None, 1, 2, None, None, None],[None for _ in range(8)],
            [None for _ in range(8)],[None for _ in range(8)]]
    reversi.load_game(2, grid)
    assert reversi.turn == 2
    assert not reversi.done
    assert reversi.grid == grid

def test_othello_load_8_2():
    """
    Tests an 8x8 Othello board: uses load_game to load a grid with at least five 
    pieces on it and verify that the state of the game was updated correctly.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    grid = [[None for _ in range(8)], [None for _ in range(8)],
            [None for _ in range(8)], [None, None, 1, 1, 1, None, None, None],
            [None, None, None, 1, 2, None, None, None],[None for _ in range(8)],
            [None for _ in range(8)],[None for _ in range(8)],
            [None for _ in range(8)]]
    with pytest.raises(ValueError):
        reversi.load_game(2, grid)

def test_othello_load_8_3():
    """
    Tests an 8x8 Othello board: uses load_game to load a grid with at least five 
    pieces on it and verify that the state of the game was updated correctly.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    grid = [[None for _ in range(8)], [None for _ in range(8)],
            [None for _ in range(8)], [None, None, 1, 1, 1, None, None, None],
            [None, None, None, 1, 2, None, None, None],[None for _ in range(8)],
            [None for _ in range(8)],[None for _ in range(8)]]
    with pytest.raises(ValueError):
        reversi.load_game(3, grid)

def test_othello_load_8_4():
    """
    Tests an 8x8 Othello board: uses load_game to load a grid with at least five 
    pieces on it and verify that the state of the game was updated correctly.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    grid = [[None for _ in range(8)], [None for _ in range(8)],
            [None for _ in range(8)],
            [None, None, None, 1, 1, None, None, None],
            [None, None, None, 1, 2, None, None, None],[None for _ in range(8)],
            [None for _ in range(8)],[None for _ in range(8)],
            [None for _ in range(8)]]
    with pytest.raises(ValueError):
        reversi.load_game(2, grid)

def test_turn_skip_1():
    """
    Tests an 4x4 Othello board: uses load_game to load a grid with the case that
    does not allow to make a move for a player 2, so they need to skip their
    move.
    """
    reversi = Reversi(side=4, players=2, othello=True)
    grid = [[1, 1, 1, None], [1, 1, 1, None], [None, 1, 2, None],
            [None, None, None, None]]
    reversi.load_game(1, grid)
    assert reversi.turn == 1
    reversi.apply_move((2, 0))
    assert reversi.turn == 1

def helper_stimulate(reversi: "Reversi", legal: Set[Tuple[int, int]]) -> None:
    """
    Check that the original game state has been preserved.

    Arguments:
        reversi[Reversi]: the object Reversi - the board created with given 
        parameters
        [Set[Tuple[int, int]]]: the list of legal moves to fill the 
        center of the board
    """
    grid_orig = reversi.grid
    assert reversi.grid == grid_orig
    assert reversi.turn == 1
    assert set(reversi.available_moves) == legal
    assert not reversi.done
    assert reversi.outcome == []

def test_simulate_move_1():
    """
    Test simulating a move that doesn't end the game
    """

    reversi = Reversi(side=8, players=2, othello=True)
    grid_orig = reversi.grid
    legal = {(2, 3), (3, 2), (4, 5), (5, 4)}
    future_reversi = reversi.simulate_moves([(2, 3)])

    helper_stimulate(reversi, legal)

    legal = {(2, 2), (2, 4), (4, 2)}
    assert future_reversi.grid != grid_orig
    assert future_reversi.turn == 2
    assert set(future_reversi.available_moves) == legal
    assert not future_reversi.done
    assert future_reversi.outcome == []

def test_simulate_move_2():
    """
    Test simulating a move that results in Player 2 winning
    """
    reversi = Reversi(side=8, players=2, othello=True)
    grid_orig = reversi.grid
    legal = {(2, 3), (3, 2), (4, 5), (5, 4)}
    helper_stimulate(reversi, legal)
    future_reversi = reversi.simulate_moves([(2, 3), (2, 4), (2, 5), (4, 2), \
    (5, 5), (1, 5), (5, 3), (4, 5), (1, 4), (0, 4), (3, 5), (1, 6), (0, 5),
    (3, 6), (3, 7), (6, 3), (1, 7), (2, 6), (2, 7), (0, 6), (5, 2), (4, 1),
    (5, 4), (0, 7), (4, 0), (0, 3), (7, 3), (5, 6), (6, 4), (7, 4), (6, 6),
    (2, 2), (6, 1), (4, 7), (1, 3), (7, 7), (3, 1), (6, 2), (7, 1), (1, 2),
    (6, 5), (6, 0), (0, 1), (1, 1), (0, 0), (2, 1), (4, 6), (1, 0), (7, 0),
    (2, 0), (7, 5), (3, 2), (5, 1), (5, 7), (7, 2), (7, 6), (5, 0), (6, 7),
    (0, 2), (3, 0)])

    assert future_reversi.grid != grid_orig
    assert future_reversi.done
    assert future_reversi.outcome == [1]

def test_simulate_move_3():
    """
    Test simulating a move that results in a tie.
    """
    reversi = Reversi(side=8, players=2, othello=True)
    grid = [[1, 1, 1, 1, 1, 1, 1, None], [2, 2, 2, 2, 2, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 1, 1], [None, 2, 2, 2, 2, 2, 2, 2]]
    reversi.load_game(1, grid)
    grid_orig = reversi
    legal = {(0, 7)}
    helper_stimulate(reversi, legal)

    future_reversi = reversi.simulate_moves([(0, 7), (7, 0)])
    assert future_reversi.grid != grid_orig
    assert future_reversi.done
    assert sorted(future_reversi.outcome) == [1, 2]

def test_simulate_moves_4():
    """
    Test that calling simulate_moves with an invalid position
    raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.simulate_moves([(-1, 0)])

    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.simulate_moves([(4, 4)])

def helper_last_move(reversi: "Reversi") -> None:
    """
    Tests all parameter for non-finished game after it was updated with 
    load_game and needs only 1/few moves to finish the game.

    Arguments:
        reversi[Reversi]: the object Reversi - the board created with given 
        parameters
    """
    assert not reversi.done
    assert reversi.outcome == []

def test_one_winner_8():
    """
    An 8x8 two-player game that ends with a full board, 
    and just one player as the winner.
    """
    reversi = Reversi(side=8, players=2, othello=False)
    grid = [[2 for _ in range(8)], [1, 1, 1, 1, 1, 2, 2, 2],
            [1, 1, 1, 1, 2, 2, 2, 2], [1, 1, 1, 1, 2, 2, 2, 2],
            [1, 1, 1, 1, 2, 2, 2, 2], [1, 1, 1, 1, 2, 2, 2, 2],
            [1, 1, 1, 1, 2, 2, 2, 2], [1, 1, None, 1, 2, 2, 2, 2]]
    reversi.load_game(2, grid)
    helper_last_move(reversi)
    reversi.apply_move((7, 2))
    assert reversi.done
    assert reversi.outcome == [2]

def test_tie_8():
    """
    An 8x8 two-player game that ends with a full board, 
    and with the two players tying.
    """
    reversi = Reversi(side=8, players=2, othello=False)
    grid = [[1, 1, 1, 1, 1, 1, 2, 2], [1, 1, 1, 1, 1, 2, 2, 2],
            [1, 1, 1, 1, 2, 2, 2, 2], [1, 1, 1, 1, 2, 2, 2, 2],
            [1, 1, 1, 1, 2, 2, 2, 2], [1, 1, 1, 1, 2, 2, 2, 2],
            [1, 1, 1, 1, 2, 2, 2, 2], [1, 1, None, 1, 2, 2, 2, 2]]
    reversi.load_game(2, grid)
    helper_last_move(reversi)
    reversi.apply_move((7, 2))
    assert reversi.done
    assert sorted(reversi.outcome) == [1, 2]

def test_one_winner_7():
    """
    A 7x7 three-player game that ends with a full board, 
    and just one player as the winner.
    """
    reversi = Reversi(side=7, players=3, othello=False)
    grid = [[1 for i in range(7)], [1 for i in range(7)], [1 for i in range(7)],
            [1 for i in range(7)], [1 for i in range(7)], [1 for i in range(7)],
            [1, 1, 1, 1, 2, 3, None]]
    reversi.load_game(1, grid)
    helper_last_move(reversi)
    reversi.apply_move((6, 6))
    assert reversi.done
    assert reversi.outcome == [1]

def test_two_winner_7():
    """
    A 7x7 three-player game that ends with a full board, 
    and two of the players tying (i.e., not a three-way tie).
    """
    reversi = Reversi(side=7, players=3, othello=False)
    grid = [[3 for _ in range(7)], [None, 3, 2, 2, 2, 2, 2],
            [2 for _ in range(7)], [2 for _ in range(7)],
            [1 for _ in range(7)],[1 for _ in range(7)],
            [1, 1, 1, 1, 1, 3, None]]
    reversi.load_game(1, grid)
    helper_last_move(reversi)
    reversi.apply_move((6, 6))
    reversi.apply_move((1, 0))
    assert reversi.done
    assert sorted(reversi.outcome) == [1, 2]

def test_not_full_8():
    """
    An 8x8 two-player game that ends with a not full board, 
    and just one player as the winner.
    """
    reversi = Reversi(side=8, players=2, othello=False)
    grid = [[None, 2, 2, 2, 2, 2, 2, 1],
            [2, 2, None, None, None, None, None, None],
            [2, None, 2, None, None, None, None, None],
            [2, None, None, 2, None, None, None, None],
            [2, None, None, None, 2, None, None, None],
            [2, None, None, None, None, 2, None, None],
            [2, None, None, None, None, None, 2, None],
            [1, None, None, None, None, None, None, 1]]
    reversi.load_game(1, grid)
    print(reversi.available_moves)
    helper_last_move(reversi)
    print(reversi.available_moves)
    reversi.apply_move((0, 0))
    assert reversi.done
    assert reversi.outcome == [1]

def test_absolute_tie_9():
    """
    An 9x9 three-player game that ends with a full board and tie.
    """
    reversi = Reversi(side=9, players=3, othello=False)
    grid = [[1 for _ in range(9)], [1 for _ in range(9)], [1 for _ in range(9)],
            [2 for _ in range(9)], [2 for _ in range(9)], [2 for _ in range(9)],
            [3 for _ in range(9)], [3 for _ in range(9)],
            [3, 3, 3, 3, 3, 3, 3, 1, None]]
    reversi.load_game(3, grid)
    helper_last_move(reversi)
    reversi.apply_move((8, 8))
    assert reversi.done
    assert sorted(reversi.outcome) == [1, 2, 3]

def test_absolute_tie_not_full_9():
    """
    An 9x9 three-player game that ends with a not full board and tie.
    """
    reversi = Reversi(side=9, players=3, othello=False)
    grid = [[1 for _ in range(9)], [1 for _ in range(9)],
            [None for _ in range(9)], [2 for _ in range(9)],
            [2 for _ in range(9)], [None for _ in range(9)],
            [3 for _ in range(9)], [3, 3, 3, 3, 3, 3, 3, 1, None],
            [None for _ in range(9)]]
    reversi.load_game(3, grid)
    helper_last_move(reversi)
    reversi.apply_move((7, 8))
    assert reversi.done
    assert sorted(reversi.outcome) == [1, 2, 3]

def test_winner_not_full_9():
    """
    An 9x9 three-player game that ends with a not full board and one winner.
    """
    reversi = Reversi(side=9, players=3, othello=False)
    grid = [[None for _ in range(9)], [None for _ in range(9)],
            [None for _ in range(9)], [None for _ in range(9)],
            [None for _ in range(9)], [None for _ in range(9)],
            [None for _ in range(9)], [3, 3, 1, 2, 3, 2, 1, 1, None],
            [None for _ in range(9)]]
    reversi.load_game(3, grid)
    helper_last_move(reversi)
    reversi.apply_move((7, 8))
    assert reversi.done
    assert reversi.outcome == [3]
