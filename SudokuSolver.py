import pygame
import time
start_time = time.time()

pygame.init()
win = pygame.display.set_mode((500,500))


class Sudoku():
    def __init__(self):
        self.emptygrid = [[("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0)],
                        [("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0)],
                        [("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0)],
                        [("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0)],
                        [("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0)],
                        [("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0)],
                        [("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0)],
                        [("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0)],
                        [("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0), ("", 0)]]
        
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


    def dryrun(self):
        # performed before starting to solve
        fixedpointfound = True
        # runs until all the fixed points have been found
        while fixedpointfound:
            fixedpointfound = False
        
            for y in range(9):
                self.currenty = y
                self.rownumbers = []
                # stores the possible values for each element in a row
                self.uniquenumbers = []
                # will store the numbers in each row that can only be in one element
                for x in range(9):                        
                    self.currentx = x
                    # goes through every element in grid
                    if self.testgridfixed[y][x] == 0:
                    # if not fixed
                        self.numbers = []
                        # will store the numbers for each element that are valid

                        for n in range(9):
                            # if still numbers to go through
                            self.currentnumber = n + 1
                            self.testgrid[y][x] = self.currentnumber

                            if(self.checkRow() and self.checkColumn() and self.checkBox()):
                            # checks if the number is valid by sudoku rules
                                self.numbers.append(self.currentnumber)
    

                        if len(self.numbers) == 1:
                            # if theres only one possible value for that box
                            self.testgrid[y][x] = self.numbers[0]
                            self.testgridfixed[y][x] = 2
                            fixedpointfound = True
                        else:
                            self.testgrid[y][x] = 0

                        self.rownumbers.append([x, self.numbers])
                        # for each element, the values it can take are stored

                self.checkHiddenValueRow()
                    
            
        self.currentnumber = 0
        self.currentx = 0
        self.currenty = 0  

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

    def checkHiddenValueRow(self):
        for array in self.rownumbers:
            for number in array[1]:
                self.uniquenumbers.append(number)

        self.uniquenumbers = ([x for x in self.uniquenumbers if self.uniquenumbers.count(x)==1])

        for array in self.rownumbers:
            for x in self.uniquenumbers:

                if x in array[1]:
                    self.testgrid[self.currenty][array[0]] = x
                    self.testgridfixed[self.currenty][array[0]] = 3
                    self.fixedpointfound = True        

    def checkHiddenValueColumn(self):
        pass

    def checkHiddenValueBox(self):
        pass


Sudoku1 = Sudoku()
Sudoku1.dryrun()
Sudoku1.draw()
pygame.quit()