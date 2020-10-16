"""
Binaire rooster is een list in een list met zijde gelijk aan breedte

"""
import copy
# import time


class Binairy:

    def __init__(self, board):
        self.board = board

    def is_valid(self, nummer, position):
        # een nummer is 1 of 0 volgens de regels van het binaire spel
        row, column = position

        given_row = self.board[row]

        whole_column = []
        for i in range(len(self.board[0])):
            whole_column += [self.board[i][column]]

        if self.check(whole_column, row, nummer) and self.check(given_row, column, nummer):
            return True
        else:
            return False

    def check(self, array, column, nummer):
        if array.count(nummer) == len(self.board) / 2:
            return False

        if column > 0 and array[column - 1] == nummer:
            if column > 1 and array[column - 2] == nummer:
                return False
            if column < len(array) - 1 and array[column + 1] == nummer:
                return False

        if column < len(array) - 1 and array[column + 1] == nummer:
            if column < len(array) - 2 and array[column + 2] == nummer:
                return False
            if column > 1 and array[column - 1] == nummer:
                return False

        return True

    def find_empty_spot(self):
        for i in range(len(self.board)):  # aantal rijen
            for j in range(len(self.board[0])):  # aantal kolommen
                if self.board[i][j] == "":
                    return i, j
        return None

    def stupid_solve(self):
        empty_spot = self.find_empty_spot()
        if empty_spot is None:
            return True
        else:
            row, column = empty_spot
        for i in [0, 1]:
            if self.is_valid(i, (row, column)):
                self.board[row][column] = i
                if self.stupid_solve():
                    return True
                else:
                    self.board[row][column] = ""
        return False

    def find_all_non_empty_spot(self):
        non_empty_spots = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != "":
                    non_empty_spots.append((i, j))
        return non_empty_spots

    def up(self, position):
        row, col = position
        if row == 0:
            return False
        else:
            return row - 1, col

    def down(self, position):
        row, col = position
        if row >= len(self.board) - 1:
            return False
        else:
            return row + 1, col

    def left(self, position):
        row, col = position
        if col == 0:
            return False
        else:
            return row, col - 1

    def right(self, position):
        row, col = position
        if col >= len(self.board[0]) - 1:
            return False
        else:
            return row, col + 1

    def nb_on_spot(self, position):
        if position is False:
            return 5
        else:
            row, col = position
            return self.board[row][col]

    def place(self, nb, pos):
        row, col = pos
        self.board[row][col] = nb

    def dubble_number_check(self):
        non_empty_spots = self.find_all_non_empty_spot()
        for spot in non_empty_spots:
            nb_spot = self.nb_on_spot(spot)

            if self.up(spot):
                pos_up = self.up(spot)
                if self.nb_on_spot(pos_up) == nb_spot:
                    if self.down(spot):
                        new_pos_down = self.down(spot)
                        if new_pos_down not in non_empty_spots:
                            if nb_spot == 1:
                                self.place(0, new_pos_down)
                            else:
                                self.place(1, new_pos_down)

            if self.down(spot):
                pos_down = self.down(spot)
                if self.nb_on_spot(pos_down) == nb_spot:
                    if self.up(spot):
                        new_pos_up = self.up(spot)
                        if new_pos_up not in non_empty_spots:
                            if nb_spot == 1:
                                self.place(0, new_pos_up)
                            else:
                                self.place(1, new_pos_up)

            if self.left(spot):
                pos_left = self.left(spot)
                if self.nb_on_spot(pos_left) == nb_spot:
                    if self.right(spot):
                        new_pos_right = self.right(spot)
                        if new_pos_right not in non_empty_spots:
                            if nb_spot == 1:
                                self.place(0, new_pos_right)
                            else:
                                self.place(1, new_pos_right)

            if self.right(spot):
                pos_right = self.right(spot)
                if self.nb_on_spot(pos_right) == nb_spot:
                    if self.left(spot):
                        new_pos_left = self.left(spot)
                        if new_pos_left not in non_empty_spots:
                            if nb_spot == 1:
                                self.place(0, new_pos_left)
                            else:
                                self.place(1, new_pos_left)

    def find_all_empty_spots(self):
        spots = []
        for row in range(len(self.board)):  # aantal rijen
            for col in range(len(self.board[0])):  # aantal kolommen
                if self.board[row][col] == "":
                    spots.append((row, col))
        return spots

    def between_check(self):
        empty_spots = self.find_all_empty_spots()
        for spot in empty_spots:
            if self.nb_on_spot(self.up(spot)) == self.nb_on_spot(self.down(spot)) and isinstance(
                    self.nb_on_spot(self.up(spot)), int):
                if self.nb_on_spot(self.up(spot)) == 1:
                    self.place(0, spot)
                else:
                    self.place(1, spot)
            if self.nb_on_spot(self.left(spot)) == self.nb_on_spot(self.right(spot)) and isinstance(
                    self.nb_on_spot(self.left(spot)), int):
                if self.nb_on_spot(self.left(spot)) == 1:
                    self.place(0, spot)
                else:
                    self.place(1, spot)

    def smart_solve(self):
        old_board = copy.deepcopy(self.board)
        self.dubble_number_check()
        self.between_check()
        if self.board == old_board:
            return False
        else:
            self.smart_solve()

    def print_board(self):
        for i in range(len(self.board)):
            for x in self.board:
                if x[i] == "":
                    print(" ", end=' | ')
                else:
                    print(x[i], end=' | ')
            print()

    def correct_full_board(self):
        for row in self.board:
            if row.count(0) != len(self.board) // 2:
                return False

        for col in range(len(self.board)):
            whole_col = []
            for row in range(len(self.board)):
                whole_col.append(self.board[row][col])

            if whole_col.count(0) != len(self.board) // 2:
                return False

        return True

#
# board = [["", 0, "", "", 1, "", 0, ""],
#          ["", "", "", "", "", "", "", 1],
#          ["", "", "", "", "", "", "", ""],
#          ["", "", "", 0, "", "", 1, ""],
#          ["", "", 1, "", 1, "", "", 0],
#          [1, "", "", "", 1, "", "", ""],
#          [1, "", "", "", "", "", "", ""],
#          ["", "", "", "", "", "", 0, ""]]
#
# stupid_solve_board = Binairy(board)
# stupid_solve_board.smart_solve()
# stupid_solve_board.stupid_solve()
# start = time.time()
# stupid_solve_board.print_board()
# print("_________________________")
# stupid_solve_board.stupid_solve()
# stupid_solve_board.print_board()
# end = time.time()
# print("____________________________")
# print("time stupid solve = ",end-start)
# print("____________________________________")
# board = [["", 0, "", "", 1, "", 0, ""],
#          ["", "", "", "", "", "", "", 1],
#          ["", "", "", "", "", "", "", ""],
#          ["", "", "", 0, "", "", 1, ""],
#          ["", "", 1, "", 1, "", "", 0],
#          [1, "", "", "", 1, "", "", ""],
#          [1, "", "", "", "", "", "", ""],
#          ["", "", "", "", "", "", 0, ""]]
# smart_solve_board = Binairy(board)
# start = time.time()
# smart_solve_board.smart_solve()
# smart_solve_board.stupid_solve()
# end = time.time()
# print("time smart solve first = ", end-start)
