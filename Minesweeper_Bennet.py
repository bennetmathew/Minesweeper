# --------------------------------------------------------------------------
# Minesweeper game in Python
# Author: Bennet Mathew
# Date: 11-17-2016
# Tested with Python 3.5.2
# ---------------------------------------------------------------------------

from tkinter import *
import random


class Board:
    """
        The Board class maintains the details of the playing board such as Frames, Buttons, mines list etc.
    """

    def __init__(self, main_window):
        self.open_tile_coord_list = []  # List to keep the coordinates of all open tiles
        self.tile_number = []  # List to store indexes of tiles from 1 to 9 for loading image

        # --------- Loading Button Images Begin -----------
        for i in range(1, 9):
            self.tile_number.append(PhotoImage(file="c:\\temp\\tile_" + str(i) + ".gif"))
        self.new_game_smiley = PhotoImage(file="c:\\temp\\new_game_button.png")
        self.flag = PhotoImage(file="c:\\temp\\flag.png")
        self.won = PhotoImage(file="c:\\temp\\won.png")
        self.lost = PhotoImage(file="c:\\temp\\lost.png")
        self.plain_tile = PhotoImage(file="c:\\temp\\tile_plain.gif")
        self.mine_source = PhotoImage(file="c:\\temp\\mine_source.png")
        self.mine = PhotoImage(file="c:\\temp\\mine.png")
        self.tile_clicked = PhotoImage(file="c:\\temp\\tile_clicked.gif")
        # --------- Loading Button Images End -----------

        # --------- Creating GUI Skelton Begin -----------
        self.top_frame = Frame(main_window, bd=4, relief=SUNKEN)  # Top Frame
        self.game_button = Button(self.top_frame, image=self.new_game_smiley, command=self.new_game)
        self.bottom_frame = Frame(main_window, width=300, height=450, bd=4, relief=SUNKEN)  # Bottom Frame
        self.status_frame = Frame(main_window)  # Status Frame
        self.status_label = Label(self.status_frame, text="Let's play")

        self.top_frame.pack(fill=X, padx=10)
        self.game_button.pack()
        self.status_frame.pack(fill=X, padx=10)
        self.status_label.pack()
        self.bottom_frame.pack(fill=X, padx=10, pady=5)
        # --------- Creating GUI Skelton End -----------

        # --------- Creating Buttons Begin -----------
        self.buttons = {}  # Dictionary to store buttons and other attributes
        self.is_mine = False  # True -> Mine, False -> Not a mine
        self.click_status = 0  # Not Clicked -> 0, Clicked -> 1, Flagged -> 2
        self.nearby_mines = 0  # Stores the count of nearby mines
        button_dict_index = 0

        for i in range(9):
            rows = i
            for j in range(9):
                columns = j
                btn = Button(self.bottom_frame, command=lambda l=button_dict_index: self.left_btn_click(l), height=20, width=25, image=self.plain_tile)
                btn.bind('<Button-3>', lambda evt2, l=button_dict_index: self.right_btn_click(evt2, l))
                btn.grid(row=rows, column=columns)

                # 0 -> Button widget
                # 1 -> Mine or not (True or False)
                # 2 -> Click status (0, 1, 2)
                # 3 -> Nearby mines count
                # 4 -> (x,y) coordinates of the button

                self.buttons[button_dict_index] = [btn, self.is_mine, self.click_status, self.nearby_mines, [rows, columns]]
                button_dict_index += 1
        # --------- Creating Buttons End -----------

        # ---------- Place Mines Begin -----------
        self.mines_list = random.sample(range(0, 81), 10)
        for x in range(10):
            self.buttons[self.mines_list[x]][1] = True
        # ---------- Place Mines End -----------

        # ----------Counting number of nearby mines Begin-----------
        for x in range(81):
            self.buttons[x][3] = self.nearby_mines_count(x)
        # ----------Counting number of nearby mines End-----------

    def left_btn_click(self, index):
        """
            This method is called when user performs a left mouse click
        """
        if self.buttons[index][2] == 0:  # Checks whether button is not clicked previously
            if self.buttons[index][1] is True:  # Checks whether clicked button is a mine
                self.game_over(index)
            else:
                nearby_mines_count = self.nearby_mines_count(index)  # Check for any nearby mines
                if nearby_mines_count == 0:  # Checks whether tile is empty
                    self.buttons[index][0]["state"] = 'disabled'
                    self.open_tile(self.buttons[index][4][0], self.buttons[index][4][1])  # Calls open_tile method to display any neighboring empty locations as well until you show a location that is a mine-neighbor
                else:
                    self.buttons[index][0].config(image=self.tile_number[nearby_mines_count-1], relief=SUNKEN)
                    self.buttons[index][0].unbind('<Button-1>')
                    self.buttons[index][0].unbind('<Button-3>')
                    self.buttons[index][2] = 1
                if self.win() is True:  # Check for win
                    self.victory()
        else:
            if self.buttons[index][2] != 2:
                (self.buttons[index][0]).unbind('<Button-3>')
            elif self.buttons[index][2] == 2:
                pass

    def right_btn_click(self, evt, index):
        """
            This method is called when user performs a right mouse click
        """
        if self.buttons[index][2] == 2:  # Checks whether it is already flagged
            evt.widget["relief"] = RAISED
            self.buttons[index][2] = 0
            evt.widget.config(image=self.plain_tile)
        else:
            evt.widget.config(image=self.flag, height=20, width=25)
            self.buttons[index][2] = 2  # Flagged

    def nearby_mines_count(self, index):
        """
            This method returns the count of nearby mines. If no nearby mines found, then it will return 0
        """
        mines_count = 0
        x_cord = self.buttons[index][4][0]
        y_cord = self.buttons[index][4][1]
        for x in range(x_cord - 1, x_cord + 2):
            for y in range(y_cord - 1, y_cord + 2):
                if -1 < x < 9 and -1 < y < 9 and not (x == x_cord and y == y_cord):
                    if self.buttons[x * 9 + y][1] is True:
                        mines_count += 1
        return mines_count

    def game_over(self, index):
        """
            This method is called when player loses a game
        """
        self.game_button.config(image=self.lost)
        self.status_label.config(text='You just lost the game')
        self.buttons[index][0].config(image=self.mine_source)
        self.buttons[index][0].config(relief=SUNKEN)
        self.buttons[index][0].unbind('<Button-3>')
        self.buttons[index][0].config(command='')
        for i, val in enumerate(self.mines_list):
            if val != index:
                self.buttons[val][0].config(image=self.mine)
                self.buttons[val][0]["relief"] = SUNKEN
        self.disable_board()

    def open_tile(self, row, column):
        """
            This is a recursive method called to display any neighboring empty locations
            as well until you show a location that is a mine-neighbor
        """
        index = self.convert_coords_to_index(row, column)
        if self.buttons[index][3] > 0 and self.buttons[index][2] is not 2:
            self.buttons[index][0].config(image=self.tile_number[self.buttons[index][3] - 1])
            self.buttons[index][0].unbind('<Button-3>')
            self.buttons[index][2] = 1
        else:
            for x in range(row - 1, row + 2):
                for y in range(column - 1, column + 2):
                    if -1 < x < 9 and -1 < y < 9:
                        coord_to_index = self.convert_coords_to_index(x, y)
                        if (x, y) not in self.open_tile_coord_list and self.buttons[coord_to_index][2] is not 2:
                            self.buttons[coord_to_index][0].config(image=self.tile_clicked, relief=SUNKEN)
                            self.buttons[coord_to_index][0].unbind('<Button-3>')
                            self.buttons[coord_to_index][2] = 1
                            self.open_tile_coord_list.append((x, y))
                            self.open_tile(x, y)

    def convert_coords_to_index(self, x, y):
        """
            Method to convert (x,y) coordinates to corresponding 1D location
        """
        return x * 9 + y

    def win(self):
        """
            Method to check whether player won or not.
        """
        count = 0
        for index in range(81):
            if self.buttons[index][2] == 1 and self.buttons[index][1] is not True:
                count += 1
        if count == 71:
            return True
        else:
            return False

    def disable_board(self):
        """
            Method used to disable the board so that user cannot click on any tiles
        """
        for i in range(81):
            self.buttons[i][0].unbind('<Button-3>')
            self.buttons[i][0].config(command='', relief=SUNKEN)

    def victory(self):
        """
            This method is called when user wins a game
        """
        self.game_button.config(image=self.won)
        self.status_label.config(text='Hooray! You Won!')
        self.disable_board()

    def new_game(self):
        """
            This method is used to reset the game so that the board is ready for a new game
        """
        self.open_tile_coord_list = []
        self.game_button.config(image=self.new_game_smiley)
        self.status_label.config(text="Let's play")

        self.is_mine = False
        self.click_status = 0  # Not Clicked --> 0, Clicked --> 1, Flagged --> 2
        self.nearby_mines = 0
        button_dict_index = 0

        for i in range(9):
            rows = i
            for j in range(9):
                columns = j
                btn = Button(self.bottom_frame, command=lambda l=button_dict_index: self.left_btn_click(l), height=20, width=25, image=self.plain_tile)
                btn.bind('<Button-3>', lambda evt2, l=button_dict_index: self.right_btn_click(evt2, l))
                btn.grid(row=rows, column=columns)
                self.buttons[button_dict_index] = [btn, self.is_mine, self.click_status, self.nearby_mines, [rows, columns]]
                button_dict_index += 1

        self.mines_list = random.sample(range(0, 81), 10)
        for x in range(10):
            self.buttons[self.mines_list[x]][1] = True

        for x in range(81):
            self.buttons[x][3] = self.nearby_mines_count(x)


def main():
    window = Tk()
    window.title("Minesweeper")  # Sets the window title
    window.geometry("306x316")  # Setting the width and height for the window
    window.resizable(0, 0)  # Disables resizing of the window
    board = Board(window)  # Creates game instance
    window.mainloop()


if __name__ == "__main__":
    main()
