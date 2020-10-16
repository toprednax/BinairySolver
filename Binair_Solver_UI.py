from tkinter import *
import Binaire_Solver as bs
import Squares_recognition as sr


class UI:
    def __init__(self):
        self.master = Tk()

    def ask_dim(self):
        s = Canvas(self.master, width=100, height=300)
        s.pack()
        text = Label(s, text="Enter the dimension of the binary board")
        dim = Entry(s)
        dim.insert(0, "for example 6x6")
        enter = Button(s, text="Start", command=lambda: self.get(dim, s))
        photo = Button(s, text="take\npicture", command=lambda: self.take_photo(s))

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
        x_place = dims.index('x')
        row = dims[0:x_place]
        col = dims[x_place+1:]
        error_text = None
        if not row.isdigit() or not col.isdigit():
            error_text = "Wrong input, use the correct notation!"

        elif row != col:
            error_text = "Wrong input, the board must be a square"

        elif int(row) % 2 != 0 or int(col) % 2 != 0:
            error_text = "Wrong input, only even numbers allowed"

        if error_text is not None:
            error = Toplevel()
            error.wm_title("ERROR")
            text = Label(error, text=error_text)
            text.grid(column=0, row=0)
            ok = Button(error, text="Okay", command=error.destroy)
            ok.grid(row=1, column=0)
            return
        else:
            dimension = (int(row), int(col))
            s.destroy()
            self.make_grid(dimension)

    def make_grid(self, dimension):
        w = Canvas(self.master, width=410, height=680)
        all_btns = dict()
        for row in range(dimension[0]):
            for column in range(dimension[1]):
                colour = "white"
                all_btns['btn{0}'.format((row, column))] = Button(w, width=16 - dimension[0]-2, height=(16-dimension[0])//2 -1, bg=colour, text="",
                                                                  font=("Purisa", 15))
                all_btns['btn{0}'.format((row, column))].configure(
                    command=lambda button=all_btns['btn{0}'.format((row, column))]: self.btn_click(button))
                all_btns['btn{0}'.format((row, column))].grid(row=row, column=column)

        s = Canvas(self.master,width = 410, height = 300)
        rows = dimension[0]
        columns = dimension[1]
        btn_solve = Button(s, width=12, height=3, bg='green', text="Solve", fg='white')
        btn_solve.configure(command=lambda: self.solve(dimension, all_btns))
        btn_solve.grid(row=rows + 1, column=columns // 2)

        btn_clear = Button(s, width=12, height=3, bg='red', text='Clear')
        btn_clear.configure(command=lambda: self.clear_grid(all_btns))
        btn_clear.grid(row=rows + 1, column=(columns // 2) - 1)

        btn_quit = Button(s, width=12, height=3, text="Quit", command=self.master.destroy)
        btn_quit.grid(row=rows + 1, column=0)

        btn_dimension = Button(s, width=12, height=3, text="Change\ndimension",
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
        board_to_solve.smart_solve()
        board_to_solve.stupid_solve()
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


B = UI()
B.ask_dim()
mainloop()
