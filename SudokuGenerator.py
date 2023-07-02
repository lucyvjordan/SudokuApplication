# Generates a filled Sudoku grid

import random

class SudokuGenerator():

    def __init__(self):

        self.grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.currentcolumn = 0
        self.currentrow = 0
        self.gridsize = 9


    def generate(self):
        self.numbers = sorted(self.numbers, key=lambda k: random.random())
        self.grid[0] = self.numbers
        # shuffles the numbers 1-9 randomly and sets it as the first row


        self.numbers = sorted(self.numbers, key=lambda k: random.random())
        self.currentrow = 1
        self.currentcolumn = 0
        # shuffles the numbers 1-9 randomly again and sets the current row and column
        ''' the numbers 1-9 are shuffled here again so that when iterating through the numbers 1-9 for each box
        to see which number fits in that box according to sudoku rules, the order in which it goes through the 
        numbers is random which decreases the chance of getting repeated grids '''

        while True:
            
            if self.grid[self.currentrow][self.currentcolumn] != self.numbers[-1]:
                # if there are still numbers to go through for that box
                if self.grid[self.currentrow][self.currentcolumn] == 0:
                    self.grid[self.currentrow][self.currentcolumn] = self.numbers[0]
                    # if that box currently contains a 0, then it hasnt been tested yet and so is set to the first number in the numbers array
                else:
                    self.grid[self.currentrow][self.currentcolumn] = self.numbers[self.numbers.index(self.grid[self.currentrow][self.currentcolumn])+1]
                    # otherwise, it finds the number in the numbers array that is after the current number the box contains
                self.currentnumber = self.grid[self.currentrow][self.currentcolumn]
                
                if(self.checkRow() and self.checkColumn() and self.checkBox()):
                # checks if the number is valid by sudoku rules
                    self.toNextBox()

            else:
                self.toPreviousBox()


    def checkRow(self):
        # checks current row for another instance of the current number

        if self.grid[self.currentrow].count(self.currentnumber) > 1:
            return False
        return True


    def checkColumn(self):
        # checks current column for another instance of the current number

        count = 0
        for y in range(len(self.grid)):
            if self.currentnumber == self.grid[y][self.currentcolumn]:
                count += 1
        if count > 1:
            return False
        return True


    def checkBox(self):
        # checks current box for another instance of the current number
        topleftbox = [0,0]

        topleftbox[0] = self.currentcolumn - (self.currentcolumn % 3)
        topleftbox[1] = self.currentrow - (self.currentrow % 3)
        # finds top left of box by subtracting mod of 3 (as there are 3 lines per box)
        count=0

        for i in range(3):
            for j in range(3):
                if self.grid[topleftbox[1] + i][topleftbox[0]+j] == self.currentnumber:
                    count += 1
        # goes through each of the 9 elements of box

        if count > 1:
            return False
        return True


    def toNextBox(self):
        if self.currentcolumn == self.gridsize - 1:
            if self.currentrow == self.gridsize - 1:
            # if in the bottom right of the box, then the sudoku is solved

                for i in range(9):
                    print(self.grid[i])
                quit()
            else:
                self.currentrow += 1
                self.currentcolumn = 0
                self.numbers = sorted(self.numbers, key=lambda k: random.random())
                # if in the rightmost column, go down a row
        else:
            self.currentcolumn += 1


    def toPreviousBox(self):
        self.grid[self.currentrow][self.currentcolumn] = 0

        if self.currentcolumn == 0:
            self.currentrow -= 1
            self.currentcolumn = 8
        # if in leftmost column, go up a row
        else:
            self.currentcolumn -= 1


if __name__ == "__main__":
    # this is true when the program starts running
    sudoku = SudokuGenerator()
    sudoku.generate()
    # keeps the menu running