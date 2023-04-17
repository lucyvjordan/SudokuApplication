import pygame
import time
start_time = time.time()
clock = pygame.time.Clock()

pygame.init()
win = pygame.display.set_mode((500,500))


class Sudoku():
    def __init__(self):
        
        self.testgridold = [[0, 0, 0, 2, 0, 6, 0, 4, 0],
                        [5, 0, 0, 3, 0, 0, 0, 1, 0],
                        [7, 6, 0, 1, 5, 4, 0, 0, 0],
                        [0, 0, 3, 0, 0, 8, 9, 6, 2],
                        [9, 0, 5, 6, 7, 2, 4, 0, 3],
                        [8, 2, 0, 0, 3, 9, 0, 0, 7],
                        [0, 3, 0, 7, 0, 5, 0, 0, 6],
                        [0, 9, 7, 8, 0, 0, 5, 3, 0],
                        [0, 5, 0, 0, 6, 0, 8, 0, 0]]
        
        self.testgridfixedold = [[0, 0, 0, 1, 0, 1, 0, 1, 0],
                        [1, 0, 0, 1, 0, 0, 0, 1, 0],
                        [1, 1, 0, 1, 1, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 1, 1, 1, 1],
                        [1, 0, 1, 1, 1, 1, 1, 0, 1],
                        [1, 1, 0, 0, 1, 1, 0, 0, 1],
                        [0, 1, 0, 1, 0, 1, 0, 0, 1],
                        [0, 1, 1, 1, 0, 0, 1, 1, 0],
                        [0, 1, 0, 0, 1, 0, 1, 0, 0]]
        

        self.testgrid = [[0, 0, 0, 0, 6, 0, 0, 0, 0],
                        [4, 0, 8, 0, 0, 0, 0, 5, 0],
                        [0, 0, 5, 0, 0, 0, 9, 2, 7],
                        [6, 0, 0, 0, 4, 3, 0, 0, 5],
                        [0, 0, 0, 0, 0, 0, 0, 1, 8],
                        [9, 0, 0, 0, 5, 7, 0, 0, 2],
                        [0, 0, 6, 0, 0, 0, 3, 7, 9],
                        [1, 0, 9, 0, 0, 0, 0, 6, 0],
                        [0, 0, 0, 0, 7, 0, 0, 0, 0]]
        
        self.testgridfixed = [[0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [1, 0, 1, 0, 0, 0, 0, 1, 0],
                        [0, 0, 1, 0, 0, 0, 1, 1, 1],
                        [1, 0, 0, 0, 1, 1, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 1, 1],
                        [1, 0, 0, 0, 1, 1, 0, 0, 1],
                        [0, 0, 1, 0, 0, 0, 1, 1, 1],
                        [1, 0, 1, 0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 1, 0, 0, 0, 0]]     
        
        self.testgrid17 = [[0, 0, 1, 0, 4, 0, 0, 0, 0],
                        [2, 0, 0, 0, 0, 0, 0, 6, 0],
                        [0, 0, 0, 0, 8, 0, 5, 0, 0],
                        [0, 0, 0, 2, 0, 0, 1, 0, 0],
                        [0, 8, 0, 0, 0, 0, 4, 0, 0],
                        [3, 0, 0, 6, 0, 0, 0, 0, 0],
                        [0, 4, 0, 0, 5, 0, 0, 7, 0],
                        [0, 0, 0, 3, 0, 0, 0, 2, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        self.testgridfixed17 = [[0, 0, 1, 0, 4, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0, 0, 1, 0, 0],
                        [0, 1, 0, 0, 0, 0, 1, 0, 0],
                        [1, 0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 1, 0, 0, 1, 0],
                        [0, 0, 0, 1, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]]           

        self.currenty = 0
        self.currentx = 0
        self.currentnumber = 0

        # will store the numbers currently in the boxes, second element of tuple is whether it is given/fixed or not
        self.origin = [25,25]
        # origin is the top left of the grid, so it can be moved without changing all drawn elements
        self.font = pygame.font.SysFont('Consolas', 25, bold=False)        
        self.boldfont = pygame.font.SysFont('Consolas', 25, bold=True)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.returning = False
        self.solving = True

            
    def draw(self):
        running = True
        while running:
            pygame.display.set_caption("Sudoku Solver")
            win.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.solving:
                self.solve()
            else:
                print("time: %s" %(time.time()-start_time))
        
            for y in range(len(self.testgrid)):
                for x in range(len(self.testgrid[y])):
                    # goes through every element of the grid
                    pygame.draw.rect(win, self.black, (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 1)
                    # draws each elements box
                    
                    if self.testgridfixed[y][x] == 1:
                        text = self.boldfont.render(str(self.testgrid[y][x]), False, self.black) 
                    
                    elif self.testgridfixed[y][x] == 2:
                        text = self.boldfont.render(str(self.testgrid[y][x]), False, self.red) 
                    
                    elif self.testgridfixed[y][x] == 3:
                        text = self.boldfont.render(str(self.testgrid[y][x]), False, self.blue) 
                                      
                    else:
                        text = self.font.render(str(self.testgrid[y][x]), False, self.green) 
                    # the number will be bold if it is fixed
                    text_rect = text.get_rect(center=(self.origin[0]+25+(x*50) , self.origin[1]+25+(y*50)))
                    win.blit(text, text_rect)
                    # draws each elements number

            for y in range(3):
                for x in range(3):
                    pygame.draw.rect(win, self.black, (self.origin[0]+(x*150), self.origin[1]+(y*150), 150, 150), 4)
                    # draws the thicker 3x3 boxes

            pygame.display.update()


    def solve(self):
        if self.testgridfixed[self.currenty][self.currentx] == 0:
        # if not fixed

            self.returning = False
            if self.testgrid[self.currenty][self.currentx] < 9:
                # if still numbers to go throguh
                self.testgrid[self.currenty][self.currentx] += 1
                self.currentnumber = self.testgrid[self.currenty][self.currentx]
            
                if(self.checkRow() and self.checkColumn() and self.checkBox()):
                # checks if the number is valid by sudoku rules
                    #nextbox
                    self.toNextBox()

            else:
                #previous box
                self.toPreviousBox()
        
        else:
            if self.returning:
                # if returning and current box is fixed, keep returning
                self.toPreviousBox()

            else:
                # if the current box is fixed and not returning, skip this box
                self.toNextBox()


    def checkRow(self):
        # checks current row for another instance of the current number

        if self.testgrid[self.currenty].count(self.currentnumber) > 1:
            return False
        return True


    def checkColumn(self):
        # checks current column for another instance of the current number

        count = 0
        for y in range(len(self.testgrid)):
            if self.currentnumber == self.testgrid[y][self.currentx]:
                count += 1
        if count > 1:
            return False
        return True


    def checkBox(self):
        # checks current box for another instance of the current number
        topleftbox = [0,0]

        topleftbox[0] = self.currentx - (self.currentx % 3)
        topleftbox[1] = self.currenty - (self.currenty % 3)
        # finds top left of box by subtracting mod of 3 (as there are 3 lines per box)
        count=0

        for i in range(3):
            for j in range(3):
                if self.testgrid[topleftbox[1] + i][topleftbox[0]+j] == self.currentnumber:
                    count += 1
        # goes through each of the 9 elements of box

        if count > 1:
            return False
        return True


    def toNextBox(self):
        if self.currentx == 8:
            if self.currenty == 8:
            # if in the bottom right of the box, then the sudoku is solved
                self.solving = False
            else:
                self.currenty += 1
                self.currentx = 0
                # if in the rightmost column, go down a row
        else:
            self.currentx += 1


    def toPreviousBox(self):
        if self.testgridfixed[self.currenty][self.currentx] == 0:
            self.testgrid[self.currenty][self.currentx] = 0
        # if current box isnt fixed, reset box to 0
        if self.currentx == 0:
            if self.currenty == 0:
                # if trying to go to previous box from top left of box, there is no solution
                self.solving = False
            else:
                self.currenty -= 1
                self.currentx = 8
        # if in leftmost column, go up a row
        else:
            self.currentx -= 1
        self.returning = True  


    def checkHiddenPointRow(self, index):
        # checks whether there are any hidden points in the current row
        self.uniquenumbers = []
        # will store a list of all the numbers that only occur once

        for array in self.testgrid[index]:
            for number in array:
                self.uniquenumbers.append(number)

        self.uniquenumbers = ([x for x in self.uniquenumbers if self.uniquenumbers.count(x)==1])
        # gets rid of all the numbers that occur more than once in the array

        pointfound = False

        for a in range (len(self.testgrid[index])):
            # a will refer to the current column in the row (index)
            for x in self.uniquenumbers:
                if x in self.testgrid[index][a]:
                # goes through every number that is unique in the row, and checks it against the numbers that are valid for the current element

                    if len(self.testgrid[index][a]) != 1:
                        # if there are other numbers that are valid for the element with the unique number, the other numbers are removed
                        self.testgrid[index][a] = [x]
                        self.testgridfixed[index][a] = 3
                        # the element becomes a hidden fixed point

                        self.removing(x, index, a)
                        pointfound = True

        if pointfound:
            self.hiddenpointfound = True
            # means that hidden points will continue to be checked for


    def checkHiddenPointColumn(self, index):
        # checks whether there are any hidden points in the current column
        self.uniquenumbers = []
        # will store a list of all the numbers that only occur once

        for j in range(len(self.testgrid)):
            for number in self.testgrid[j][index]:
                # takes all the numbers in the current column (index = current column)
                self.uniquenumbers.append(number)
                
        self.uniquenumbers = ([x for x in self.uniquenumbers if self.uniquenumbers.count(x)==1])
        # gets rid of all the numbers that occur more than once in the array

        pointfound = False

        for a in range (len(self.testgrid)):
            # a will refer to the current row in the column (index)
            for x in self.uniquenumbers:
                if x in self.testgrid[a][index]:
                # goes through every number that is unique in the row, and checks it against the numbers that are valid for the current element

                    if len(self.testgrid[a][index]) != 1:
                    # if there are other numbers that are valid for the element with the unique number, the other numbers are removed
                        
                        self.testgrid[a][index] = [x]
                        self.testgridfixed[a][index] = 3
                        # the element becomes a hidden fixed point

                        self.removing(x, a, index)
                        pointfound = True

        if pointfound:
            self.hiddenpointfound = True
            # means that hidden points will continue to be checked for


    def checkHiddenPointBox(self, index):
        # not coded yet
        pass


    def removing(self, toRemove, row, column):
        # a function which removes a hidden points value from the possible values of the elements in its row, box, and column
        for i in range(9):
            # goes through every line of row and column
            if toRemove in self.testgrid[row][i]:
                # iteration of the for loop refers to the column
                if column == i:
                    pass
                # if it is the fixed point, it should not be removed
                else:
                    self.testgrid[row][i].remove(toRemove)
                    # the number is removed from that elements array of possible values

                    if len(self.testgrid[row][i]) == 1:
                        # if the element that has been removed from now has a length of 1, it becomes a new fixed point, and is passed recursively into this function to be removed from its neighbours
                        self.testgridfixed[row][i] = 3
                        self.removing(self.testgrid[row][i][0], row, i)
                    
            if toRemove in self.testgrid[i][column]:
                # iteration of the for loop refers to the row
                if row == i:
                    pass
                # if it is the fixed point, it should not be removed
                else:
                    self.testgrid[i][column].remove(toRemove)
                    # the number is removed from that elements array of possible values

                    if len(self.testgrid[i][column]) == 1:
                        # if the element that has been removed from now has a length of 1, it becomes a new fixed point, and is passed recursively into this function to be removed from its neighbours
                        self.testgridfixed[i][column] = 3
                        self.removing(self.testgrid[i][column][0], i, column)

        # will remove the value also from all the other elements in its box
        topleftbox = [0,0]
        topleftbox[0] = column - (column % 3)
        topleftbox[1] = row - (row % 3)
        # finds top left of box by subtracting mod of 3 (as there are 3 lines per box)

        for i in range(3):
            for j in range(3):
                # goes through every element in the box
                if toRemove in self.testgrid[topleftbox[1] + i][topleftbox[0] + j]:
                    if topleftbox[1] + i == row and topleftbox[0] + j == column:
                        pass
                    # if it is the hidden point, it should not be removed
                    else:
                        self.testgrid[topleftbox[1] + i][topleftbox[0] + j].remove(toRemove)

                        if len(self.testgrid[topleftbox[1] + i][topleftbox[0]+j]) == 1:
                            # if the element that has been removed from now has a length of 1, it becomes a new fixed point, and is passed recursively into this function to be removed from its neighbours                  
                            self.testgridfixed[topleftbox[1] + i][topleftbox[0] + j] = 3
                            self.removing(self.testgrid[topleftbox[1] + i][topleftbox[0] + j][0], topleftbox[1] + i, topleftbox[0]+j)


    def dryrun(self):
        for y in range(9):
            self.currenty = y
            for x in range(9):
                self.currentx = x
                # goes through each element
                if self.testgridfixed[y][x] == 0:
                # if not fixed
                    self.numbers = []
                    # will store all the numbers that are valid for that element

                    for n in range(9):
                        # if still numbers to go through
                        self.currentnumber = n + 1
                        self.testgrid[y][x] = self.currentnumber

                        if(self.checkRow() and self.checkColumn() and self.checkBox()):
                        # checks if the number is valid by sudoku rules
                            self.numbers.append(self.currentnumber)
                    

                    self.testgrid[y][x] = self.numbers
                    # that elements index in the array is set to all the possible numbers it can take

        for p in range (len(self.testgrid)):
            for q in range(len(self.testgrid[p])):
                if isinstance(self.testgrid[p][q], int):
                    self.testgrid[p][q] = [self.testgrid[p][q]]
        # all the given fixed points are currently stored as integers, so they are changed to be stored as a single element list

        for i in range(9):
            for j in range(9):
                if len(self.testgrid[i][j]) == 1 and self.testgridfixed[i][j] == 0:
                    self.testgridfixed[i][j] = 3
                    self.removing(self.testgrid[i][j][0], i, j)
        # first checks to see if there are any elements with only one possible value
        
        self.hiddenpointfound = True
        while self.hiddenpointfound:
            # while there are still hidden points to be found
            self.hiddenpointfound = False


            for i in range(9):
                self.checkHiddenPointRow(i)
                self.checkHiddenPointColumn(i)
                #self.checkHiddenPointBox(i)

        
        for i in range(len(self.testgrid)):
            for j in range(len(self.testgrid)):
                if len(self.testgrid[i][j]) == 1:
                    self.testgrid[i][j] = self.testgrid[i][j][0]
                else:
                    self.testgrid[i][j] = 0
        # goes through the arrays of every elements possible numbers, if it is not a fixed point, it is set to 0

        self.currentx = 0
        self.currenty = 0
        self.currentnumber = 0
        # the current values are reset
        self.draw()


Sudoku1 = Sudoku()
Sudoku1.dryrun()
pygame.quit()