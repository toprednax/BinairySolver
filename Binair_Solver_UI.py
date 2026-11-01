import tkinter as tk
from tkinter import messagebox

import Binaire_Solver as bs
import Squares_recognition as sr


class UI:
    def __init__(self):
        self.master = tk.Tk()

    def ask_dim(self):
        s = tk.Canvas(self.master, width=100, height=300)
        s.pack()
        text = tk.Label(s, text="Enter the dimension of the binary board")
        dim = tk.Entry(s)
        dim.insert(0, "for example 6x6")
        enter = tk.Button(s, text="Start", command=lambda: self.get(dim, s))
        photo = tk.Button(s, text="take\npicture", command=lambda: self.take_photo(s))

        text.pack()
        dim.pack()
        enter.pack()
        photo.pack()

    def take_photo(self,s):
        grid = sr.binary_photo()
        s.destroy()
        dimension = (len(grid),len(grid))
        btns = self.make_grid(dimension)
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                btn = btns['btn{0}'.format((row, col))]
                if grid[row][col] == 0:
                    btn['text'] = 0
                elif grid[row][col] == 1:
                    btn['text'] = 1
                else:
                    continue

    def get(self, dim, s):
        dims = dim.get()
        parts = dims.lower().split("x")
        row, col = parts if len(parts) == 2 else ("", "")
        error_text = None
        if not row.isdigit() or not col.isdigit():
            error_text = "Wrong input, use the correct notation!"

        elif row != col:
            error_text = "Wrong input, the board must be a square"

        elif int(row) % 2 != 0 or int(col) % 2 != 0:
            error_text = "Wrong input, only even numbers allowed"

        if error_text is not None:
            error = tk.Toplevel()
            error.wm_title("ERROR")
            text = tk.Label(error, text=error_text)
            text.grid(column=0, row=0)
            ok = tk.Button(error, text="Okay", command=error.destroy)
            ok.grid(row=1, column=0)
            return
        else:
            dimension = (int(row), int(col))
            s.destroy()
            self.make_grid(dimension)

    def make_grid(self, dimension):
        w = tk.Canvas(self.master, width=410, height=680)
        all_btns = dict()
        for row in range(dimension[0]):
            for column in range(dimension[1]):
                colour = "white"
                all_btns['btn{0}'.format((row, column))] = tk.Button(w, width=max(2, 14 - dimension[0]), height=max(1, (16-dimension[0])//2 -1), bg=colour, text="",
                                                                  font=("Purisa", 15))
                all_btns['btn{0}'.format((row, column))].configure(
                    command=lambda button=all_btns['btn{0}'.format((row, column))]: self.btn_click(button))
                all_btns['btn{0}'.format((row, column))].grid(row=row, column=column)

        s = tk.Canvas(self.master,width = 410, height = 300)
        rows = dimension[0]
        columns = dimension[1]
        btn_solve = tk.Button(s, width=12, height=3, bg='green', text="Solve", fg='white')
        btn_solve.configure(command=lambda: self.solve(dimension, all_btns))
        btn_solve.grid(row=rows + 1, column=columns // 2)

        btn_clear = tk.Button(s, width=12, height=3, bg='red', text='Clear')
        btn_clear.configure(command=lambda: self.clear_grid(all_btns))
        btn_clear.grid(row=rows + 1, column=(columns // 2) - 1)

        btn_quit = tk.Button(s, width=12, height=3, text="Quit", command=self.master.destroy)
        btn_quit.grid(row=rows + 1, column=0)

        btn_dimension = tk.Button(s, width=12, height=3, text="Change\ndimension",
                               command=lambda: [s.destroy(),w.destroy(), self.ask_dim()])
        btn_dimension.grid(row=rows + 1, column=columns - 1)
        w.pack(side = "top")
        s.pack(side= "bottom")
        return all_btns

    def clear_grid(self, all_btns):
        for btn in all_btns.values():
            btn['text'] = ""

    def solve(self, dimension, all_btns):
        grid = self.create_grid(dimension, all_btns)
        board_to_solve = bs.Binairy(grid)
        if not board_to_solve.smart_solve() or not board_to_solve.stupid_solve():
            messagebox.showerror("Binary solver", "This board has no valid solution.")
            return
        self.display_grid(grid, all_btns)

    def display_grid(self, grid, all_btns):
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                button = all_btns['btn{0}'.format((row, col))]
                button['text'] = grid[row][col]

    def create_grid(self, dimension, all_btns):
        grid = []
        current_row = []
        col = 0
        for button in all_btns.values():
            current_row.append(button['text'])
            col += 1
            if col == dimension[1]:
                grid.append(current_row)
                col = 0
                current_row = []
        return grid

    def btn_click(self, btn):
        if btn['text'] == "":
            btn['text'] = 0
        elif btn['text'] == 0:
            btn['text'] = 1
        elif btn['text'] == 1:
            btn['text'] = ""


if __name__ == "__main__":
    app = UI()
    app.ask_dim()
    app.master.mainloop()
