"""Solver for binary (Takuzu) puzzles.

Boards are square lists containing ``0``, ``1`` and ``""`` for empty cells.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Optional, Union


EMPTY = ""


class Binairy:
    """Solve a binary puzzle in place.

    The misspelled class name is retained for compatibility with the UI.
    """

    def __init__(self, board: list[list[Union[int, str]]]):
        self._validate_shape(board)
        self.board = board
        self.size = len(board)
        self.half = self.size // 2

    @staticmethod
    def _validate_shape(board: Sequence[Sequence[Union[int, str]]]) -> None:
        if not board or len(board) % 2:
            raise ValueError("The board size must be a positive even number")
        size = len(board)
        if any(len(row) != size for row in board):
            raise ValueError("The board must be square")
        if any(cell not in (0, 1, EMPTY) for row in board for cell in row):
            raise ValueError('Cells must contain 0, 1, or ""')

    def _column(self, column: int) -> list[Union[int, str]]:
        return [row[column] for row in self.board]

    def _line_is_valid(self, line: Sequence[Union[int, str]]) -> bool:
        if line.count(0) > self.half or line.count(1) > self.half:
            return False
        return all(
            not (line[index] == line[index + 1] == line[index + 2] != EMPTY)
            for index in range(self.size - 2)
        )

    def _complete_line_is_unique(self, line: Sequence[Union[int, str]], *, row: bool, index: int) -> bool:
        if EMPTY in line:
            return True
        peers = self.board if row else [self._column(col) for col in range(self.size)]
        return all(index == peer_index or list(line) != list(peer) for peer_index, peer in enumerate(peers))

    def is_valid(self, number: int, position: tuple[int, int]) -> bool:
        """Return whether placing *number* at *position* obeys all rules."""
        if number not in (0, 1):
            return False
        row, column = position
        if self.board[row][column] not in (EMPTY, number):
            return False

        previous = self.board[row][column]
        self.board[row][column] = number
        row_values = self.board[row]
        column_values = self._column(column)
        valid = (
            self._line_is_valid(row_values)
            and self._line_is_valid(column_values)
            and self._complete_line_is_unique(row_values, row=True, index=row)
            and self._complete_line_is_unique(column_values, row=False, index=column)
        )
        self.board[row][column] = previous
        return valid

    def check(self, array: Sequence[Union[int, str]], position: int, number: int) -> bool:
        """Compatibility helper: validate a number in a standalone line."""
        candidate = list(array)
        candidate[position] = number
        return self._line_is_valid(candidate)

    def _board_is_valid(self) -> bool:
        rows = self.board
        columns = [self._column(column) for column in range(self.size)]
        if not all(self._line_is_valid(line) for line in rows + columns):
            return False
        complete_rows = [tuple(line) for line in rows if EMPTY not in line]
        complete_columns = [tuple(line) for line in columns if EMPTY not in line]
        return len(complete_rows) == len(set(complete_rows)) and len(complete_columns) == len(set(complete_columns))

    def _best_empty_spot(self) -> tuple[Optional[tuple[int, int]], list[int]]:
        """Choose the empty cell with the fewest legal values (MRV heuristic)."""
        best_position = None
        best_candidates = [0, 1]
        for row in range(self.size):
            for column in range(self.size):
                if self.board[row][column] != EMPTY:
                    continue
                candidates = [number for number in (0, 1) if self.is_valid(number, (row, column))]
                if len(candidates) < len(best_candidates) or best_position is None:
                    best_position, best_candidates = (row, column), candidates
                if len(candidates) <= 1:
                    return best_position, best_candidates
        return best_position, best_candidates

    def find_empty_spot(self) -> Optional[tuple[int, int]]:
        position, _ = self._best_empty_spot()
        return position

    def stupid_solve(self) -> bool:
        """Solve the board with constraint-guided backtracking."""
        if not self._board_is_valid():
            return False
        position, candidates = self._best_empty_spot()
        if position is None:
            return self.correct_full_board()
        for number in candidates:
            self.place(number, position)
            if self.stupid_solve():
                return True
        self.place(EMPTY, position)
        return False

    def smart_solve(self) -> bool:
        """Repeatedly fill cells that have exactly one legal value.

        Returns ``False`` if a contradiction is found, otherwise ``True``.
        """
        if not self._board_is_valid():
            return False
        while True:
            changed = False
            for row, column in self.find_all_empty_spots():
                candidates = [number for number in (0, 1) if self.is_valid(number, (row, column))]
                if not candidates:
                    return False
                if len(candidates) == 1:
                    self.place(candidates[0], (row, column))
                    changed = True
            if not changed:
                return True

    def find_all_empty_spots(self) -> list[tuple[int, int]]:
        return [
            (row, column)
            for row in range(self.size)
            for column in range(self.size)
            if self.board[row][column] == EMPTY
        ]

    def find_all_non_empty_spot(self) -> list[tuple[int, int]]:
        return [
            (row, column)
            for row in range(self.size)
            for column in range(self.size)
            if self.board[row][column] != EMPTY
        ]

    def place(self, number: Union[int, str], position: tuple[int, int]) -> None:
        row, column = position
        self.board[row][column] = number

    def print_board(self) -> None:
        for row in self.board:
            print(" | ".join(" " if value == EMPTY else str(value) for value in row))

    def correct_full_board(self) -> bool:
        return (
            all(EMPTY not in row for row in self.board)
            and self._board_is_valid()
            and all(row.count(0) == self.half for row in self.board)
            and all(self._column(column).count(0) == self.half for column in range(self.size))
        )
