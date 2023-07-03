# Generates a filled Sudoku grid

import random
import time
import copy

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
        
        self.gridfixed = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
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

        self.backtracking = False
        self.solving = True
        self.solution = True
        self.solutioncount = 0


        self.removingValues = False
        self.removeCount = 0
        self.removeTarget = 80
        self.starttime = time.time()


    def Generate(self):
        self.numbers = sorted(self.numbers, key=lambda k: random.random())
        self.grid[0] = self.numbers
        # shuffles the numbers 1-9 randomly and sets it as the first row

        self.generating = True
        self.numbers = sorted(self.numbers, key=lambda k: random.random())
        self.currentrow = 1
        self.currentcolumn = 0
        # shuffles the numbers 1-9 randomly again and sets the current row and column
        ''' the numbers 1-9 are shuffled here again so that when iterating through the numbers 1-9 for each box
        to see which number fits in that box according to sudoku rules, the order in which it goes through the 
        numbers is random which decreases the chance of getting repeated grids '''

        self.Solve()

        self.gridfixed = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]]
        # all values in the grid start as fixed points
        
        self.RemoveNumbers()


    def Solve(self):

        self.backtracking = False
        # resets from previous iterations

        while self.solving:

            if self.gridfixed[self.currentrow][self.currentcolumn] == 0:
                # if the current number is not a fixed point then it can be changed
                self.backtracking = False
                if self.grid[self.currentrow][self.currentcolumn] != self.numbers[-1]:
                    # if there are still numbers to go through for that box
                    if self.grid[self.currentrow][self.currentcolumn] == 0:
                        self.grid[self.currentrow][self.currentcolumn] = self.numbers[0]
                        # if that box currently contains a 0, then it hasnt been tested yet and so is set to the first number in the numbers array
                    else:
                        self.grid[self.currentrow][self.currentcolumn] = self.numbers[self.numbers.index(self.grid[self.currentrow][self.currentcolumn])+1]
                        # otherwise, it finds the number in the numbers array that is after the current number the box contains
                    self.currentnumber = self.grid[self.currentrow][self.currentcolumn]
                    
                    if(self.CheckRow() and self.CheckColumn() and self.CheckBox()):
                    # checks if the number is valid by sudoku rules
                        self.ToNextBox()

                else:
                    self.ToPreviousBox()
                    # if there are no values which work for this box, then needs to backtrack
            
            else:
                if self.backtracking:
                    # if backtracking and current box is fixed, keep backtracking
                    self.ToPreviousBox()

                else:
                    # if the current box is fixed and not backtracking, skip this box
                    self.ToNextBox()
        
        if self.solution:
            return True
        return False


    def CheckRow(self):
        # checks current row for another instance of the current number

        if self.grid[self.currentrow].count(self.currentnumber) > 1:
            return False
        return True


    def CheckColumn(self):
        # checks current column for another instance of the current number

        count = 0
        for y in range(len(self.grid)):
            if self.currentnumber == self.grid[y][self.currentcolumn]:
                count += 1
        if count > 1:
            return False
        return True


    def CheckBox(self):
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


    def ToNextBox(self):
        if self.currentcolumn == self.gridsize - 1:
            if self.currentrow == self.gridsize - 1:
            # if in the bottom right of the box, then the sudoku is solved

                self.solutioncount += 1
                if self.solutioncount == 1 and self.removingValues == True:
                    self.ToPreviousBox()
                    # if we are in the process of removing values from the grid, and only one solution has been found, then backtrack
                else:
                    self.solving = False
                    # if we are not in the process of removing values, then the sudoku has been solved and the loop can stop

            else:
                self.currentrow += 1
                self.currentcolumn = 0
                # if in the rightmost column, go down a row
                if self.generating:
                    self.numbers = sorted(self.numbers, key=lambda k: random.random())
                    # if currently generating the grid, then shuffle the number arrays for the next row
        else:
            self.currentcolumn += 1
            # if not in the final column, then increment columns


    def ToPreviousBox(self):
        if self.gridfixed[self.currentrow][self.currentcolumn] == 0:
            self.grid[self.currentrow][self.currentcolumn] = 0
            # if not a fixed point, reset box to 0

        if self.currentcolumn == 0:
            if self.currentrow == 0:
                # if trying to go to previous box from top left of box, there is no solution
                self.solving = False
            else:
                self.currentrow -= 1
                self.currentcolumn = 8
                # if in leftmost column, go up a row

        else:
            self.currentcolumn -= 1
            # if not in leftmost column, decrement columns
        self.backtracking = True

    def RemoveNumbers(self):

        self.removingValues = True
        self.generating = False

        self.fullgrid = copy.deepcopy(self.grid)
        self.fullgridfixed = copy.deepcopy(self.gridfixed)
        # copy the grid so that when it is being solved there is still a copy where values are removed

        availableLocations = []
        for x in range(9):
            for y in range(9):
                availableLocations.append([y,x])
                # an array of all possible values in the grid which contain numbers
        
        attempts = 0
        # restrict number of attempts to remove values which fail so that program doesnt run forever

        removed = True

        while self.removingValues and removed:

            availableLocations = sorted(availableLocations, key=lambda k: random.random())
            # list of available locations is shuffled at start of each iteration
            removeIndex = 0
            removed = False

            while removeIndex < len(availableLocations):
                # goes through each item of array then shuffles again if a value was removed
                # so stops running when it has gone through all available locations without removing one
                
                removeLocation = availableLocations[removeIndex]

                self.grid = copy.deepcopy(self.fullgrid)
                self.gridfixed = copy.deepcopy(self.fullgridfixed)
                # copy fullgrid onto grid because grid may still contain a solution from solving in the last iteration
                # fullgrid will have the values removed that support 1 solution

                self.grid[removeLocation[0]][removeLocation[1]] = 0
                self.gridfixed[removeLocation[0]][removeLocation[1]] = 0
                # remove the value from the grid

                self.solving = True
                self.solutioncount = 0
                self.currentrow = 0
                self.currentcolumn = 0
                self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                # resetting variables needed for the solving function

                if self.Solve():
                    
                    if self.solutioncount == 1:
                        self.removeCount += 1
                        # counts how many values have been removed

                        self.fullgrid[removeLocation[0]][removeLocation[1]] = 0
                        self.fullgridfixed[removeLocation[0]][removeLocation[1]] = 0
                        # value can be removed from main grid as it creates a unique solution
                        attempts = 0
                        availableLocations.remove(removeLocation)
                        # removing this value gives a unique solution so it is removed from the full grid

                        removed = True

                    else:
                        attempts += 1
                else:
                    attempts += 1
               
                removeIndex += 1

        for i in range(self.gridsize):
            print(self.fullgrid[i])
        print("\n")
        print(self.removeCount)
        print(time.time() - self.starttime)
        # prints sudoku to terminal, how many values were removed and the time it took to generate


if __name__ == "__main__":
    # this is true when the program starts running
    sudoku = SudokuGenerator()
    sudoku.Generate()
    # keeps the sudoku generator running