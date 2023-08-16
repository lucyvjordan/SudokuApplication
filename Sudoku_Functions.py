# Generates a filled Sudoku grid

import random
import time
import copy

class SudokuFunctions():

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

        self.generating = False
        # it is not generating as soon as the instance of the class is defined

        self.removingValues = False
        self.removeCount = 0
        self.removeTarget = 0
        self.starttime = time.time()


    def Generate(self, difficulty):
        self.generating = True
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
        
        self.RemoveNumbers(difficulty)


    def Solve(self):

        self.backtracking = False
        # resets from previous iterations
        if self.removingValues:
            self.dryrun()

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
                    self.completegrid = copy.deepcopy(self.grid)
                    self.completegridfixed = copy.deepcopy(self.gridfixed)
                    # this new complete grid array will store the solution which will be used to check the players input
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

    def RemoveNumbers(self, difficulty):

        difficulties = {"EASY": 30, "MEDIUM": 45, "HARD": 60}

        self.removeTarget = difficulties[difficulty]

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

            while removeIndex < len(availableLocations) and self.removeCount < self.removeTarget:
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
                        removeIndex += 1
                        # removeIndex only incremented if value not removed so that it doesnt skip over any element in the array
                else:
                    attempts += 1
                    removeIndex += 1

        for i in range(self.gridsize):
            print(self.fullgrid[i])
        print("\n")
        print(self.removeCount)
        print(time.time() - self.starttime)
        # prints sudoku to terminal, how many values were removed and the time it took to generate

        self.grid = copy.deepcopy(self.fullgrid)
        self.gridfixed = copy.deepcopy(self.fullgridfixed)
        
        self.generating = False



    def checkHiddenPointRow(self, index):
        # checks whether there are any hidden points in the current row
        self.uniquenumbers = []
        # will store a list of all the numbers that only occur once

        for array in self.grid[index]:
            for number in array:
                self.uniquenumbers.append(number)

        self.uniquenumbers = ([x for x in self.uniquenumbers if self.uniquenumbers.count(x)==1])
        # gets rid of all the numbers that occur more than once in the array

        pointfound = False

        for a in range (len(self.grid[index])):
            # a will refer to the current column in the row (index)
            for x in self.uniquenumbers:
                if x in self.grid[index][a]:
                # goes through every number that is unique in the row, and checks it against the numbers that are valid for the current element

                    if len(self.grid[index][a]) != 1:
                        # if there are other numbers that are valid for the element with the unique number, the other numbers are removed
                        self.grid[index][a] = [x]
                        self.gridfixed[index][a] = 3
                        # the element becomes a hidden fixed point

                        self.RemoveHiddenPoint(x, index, a)
                        pointfound = True

        if pointfound:
            self.hiddenpointfound = True
            # means that hidden points will continue to be checked for


    def checkHiddenPointColumn(self, index):
        # checks whether there are any hidden points in the current column
        self.uniquenumbers = []
        # will store a list of all the numbers that only occur once

        for j in range(len(self.grid)):
            for number in self.grid[j][index]:
                # takes all the numbers in the current column (index = current column)
                self.uniquenumbers.append(number)
                
        self.uniquenumbers = ([x for x in self.uniquenumbers if self.uniquenumbers.count(x)==1])
        # gets rid of all the numbers that occur more than once in the array

        pointfound = False

        for a in range (len(self.grid)):
            # a will refer to the current row in the column (index)
            for x in self.uniquenumbers:
                if x in self.grid[a][index]:
                # goes through every number that is unique in the row, and checks it against the numbers that are valid for the current element

                    if len(self.grid[a][index]) != 1:
                    # if there are other numbers that are valid for the element with the unique number, the other numbers are removed
                        
                        self.grid[a][index] = [x]
                        self.gridfixed[a][index] = 3
                        # the element becomes a hidden fixed point

                        self.RemoveHiddenPoint(x, a, index)
                        pointfound = True

        if pointfound:
            self.hiddenpointfound = True
            # means that hidden points will continue to be checked for


    def checkHiddenPointBox(self):
        # checks whether there are any hidden points in the current box        
       
        for y in range(3):
            for x in range(3):
            # goes through every box

                self.uniquenumbers = []
                # will store a list of all the numbers that only occur once
                topleftbox = [0, 0]
                topleftbox[0] = y * 3
                topleftbox[1] = x * 3
                # finds the top left of each box, (0,0), (3,0), (6,3) etc. 

                for i in range(3):
                    for j in range(3):
                        for number in self.grid[topleftbox[0] + i][topleftbox[1] + j]:
                            self.uniquenumbers.append(number)
                # goes through each of the 9 elements of box and finds the valid numbers for each
                
                self.uniquenumbers = ([x for x in self.uniquenumbers if self.uniquenumbers.count(x)==1])
                # gets rid of all the numbers that occur more than once in the array

                pointfound = False

                for i in range(3):
                    for j in range(3):
                        # goes through every box again
                        for x in self.uniquenumbers:
                            if x in self.grid[topleftbox[0] + i][topleftbox[1] + j]:
                            # goes through every number that is unique in the box, and checks it against the numbers that are valid for the current element

                                if len(self.grid[topleftbox[0] + i][topleftbox[1] + j]) != 1:
                                # if there are other numbers that are valid for the element with the unique number, the other numbers are removed

                                    self.grid[topleftbox[0] + i][topleftbox[1] + j] = [x]
                                    self.gridfixed[topleftbox[0] + i][topleftbox[1] + j] = 3
                                    # the element becomes a hidden fixed point

                                    self.RemoveHiddenPoint(x, topleftbox[0] + i, topleftbox[1] + j)

                                    pointfound = True

                if pointfound:
                    self.hiddenpointfound = True
                    # means that hidden points will continue to be checked for


    def RemoveHiddenPoint(self, toRemove, row, column):
        # a function which removes a hidden points value from the possible values of the elements in its row, box, and column
        for i in range(9):
            # goes through every line of row and column
            if toRemove in self.grid[row][i]:
                # iteration of the for loop refers to the column
                if column == i:
                    pass
                # if it is the fixed point, it should not be removed
                else:
                    self.grid[row][i].remove(toRemove)
                    # the number is removed from that elements array of possible values

                    if len(self.grid[row][i]) == 0:
                        self.solution = False
                    # if that box has no possible values, then there is no solution

                    if len(self.grid[row][i]) == 1:
                        # if the element that has been removed from now has a length of 1, it becomes a new fixed point, and is passed recursively into this function to be removed from its neighbours
                        self.gridfixed[row][i] = 3
                        self.RemoveHiddenPoint(self.grid[row][i][0], row, i)
                    
            if toRemove in self.grid[i][column]:
                # iteration of the for loop refers to the row
                if row == i:
                    pass
                # if it is the fixed point, it should not be removed
                else:
                    self.grid[i][column].remove(toRemove)
                    # the number is removed from that elements array of possible values

                    if len(self.grid[i][column]) == 0:
                        self.solution = False
                    # if that box has no possible values, then there is no solution

                    if len(self.grid[i][column]) == 1:
                        # if the element that has been removed from now has a length of 1, it becomes a new fixed point, and is passed recursively into this function to be removed from its neighbours
                        self.gridfixed[i][column] = 3
                        self.RemoveHiddenPoint(self.grid[i][column][0], i, column)

        # will remove the value also from all the other elements in its box
        topleftbox = [0,0]
        topleftbox[0] = column - (column % 3)
        topleftbox[1] = row - (row % 3)
        # finds top left of box by subtracting mod of 3 (as there are 3 lines per box)

        for i in range(3):
            for j in range(3):
                # goes through every element in the box
                if toRemove in self.grid[topleftbox[1] + i][topleftbox[0] + j]:
                    if topleftbox[1] + i == row and topleftbox[0] + j == column:
                        pass
                    # if it is the hidden point, it should not be removed
                    else:
                        self.grid[topleftbox[1] + i][topleftbox[0] + j].remove(toRemove)

                        if len(self.grid[topleftbox[1] + i][topleftbox[0]+j]) == 0:
                            self.solution = False
                        # if that box has no possible values, then there is no solution

                        if len(self.grid[topleftbox[1] + i][topleftbox[0]+j]) == 1:
                            # if the element that has been removed from now has a length of 1, it becomes a new fixed point, and is passed recursively into this function to be removed from its neighbours                  
                            self.gridfixed[topleftbox[1] + i][topleftbox[0] + j] = 3
                            self.RemoveHiddenPoint(self.grid[topleftbox[1] + i][topleftbox[0] + j][0], topleftbox[1] + i, topleftbox[0]+j)


    def dryrun(self):
        for y in range(9):
            self.currentrow = y
            for x in range(9):
                self.currentcolumn = x
                # goes through each element
                if self.gridfixed[y][x] == 0:
                # if not fixed
                    self.numbers = []
                    # will store all the numbers that are valid for that element

                    for n in range(9):
                        # if still numbers to go through
                        self.currentnumber = n + 1
                        self.grid[y][x] = self.currentnumber

                        if(self.CheckRow() and self.CheckColumn() and self.CheckBox()):
                        # checks if the number is valid by sudoku rules
                            self.numbers.append(self.currentnumber)
                    
                    self.grid[y][x] = self.numbers
                    # that elements index in the array is set to all the possible numbers it can take

        for p in range (len(self.grid)):
            for q in range(len(self.grid[p])):
                if isinstance(self.grid[p][q], int):
                    self.grid[p][q] = [self.grid[p][q]]
        # all the given fixed points are currently stored as integers, so they are changed to be stored as a single element list

        for i in range(9):
            for j in range(9):
                if len(self.grid[i][j]) == 1 and self.gridfixed[i][j] == 0:
                    self.gridfixed[i][j] = 3
                    self.RemoveHiddenPoint(self.grid[i][j][0], i, j)
        # first checks to see if there are any elements with only one possible value
        
        self.hiddenpointfound = True
        while self.hiddenpointfound:
            # while there are still hidden points to be found
            self.hiddenpointfound = False

            for i in range(9):
                self.checkHiddenPointRow(i)
                self.checkHiddenPointColumn(i)
                self.checkHiddenPointBox()
                # index not passed to this one, because doing so would mean only boxes 1, 5, and 9 are checked
                # (index goes diagonally down and right - which works for row and column, but not for boxes)


            if self.solution == False:
                self.solving = False
                return False


        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if len(self.grid[i][j]) == 1:
                    self.grid[i][j] = self.grid[i][j][0]
                else:
                    self.grid[i][j] = 0
        # goes through the arrays of every elements possible numbers, if it is not a fixed point, it is set to 0

        self.currentcolumn = 0
        self.currentrow = 0
        self.currentnumber = 0
        # the current values are reset

        return True
