import pygame
import time

pygame.init()
win = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()



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
        
        self.testgrid = [[0, 0, 0, 2, 0, 6, 0, 4, 0],
                        [5, 0, 0, 3, 0, 0, 0, 1, 0],
                        [7, 6, 0, 1, 5, 4, 0, 0, 0],
                        [0, 0, 3, 0, 0, 8, 9, 6, 2],
                        [9, 0, 5, 6, 7, 2, 4, 0, 3],
                        [8, 2, 0, 0, 3, 9, 0, 0, 7],
                        [0, 3, 0, 7, 0, 5, 0, 0, 6],
                        [0, 9, 7, 8, 0, 0, 5, 3, 0],
                        [0, 5, 0, 0, 6, 0, 8, 0, 0]]
        
        self.testgridfixed = [[0, 0, 0, 1, 0, 1, 0, 1, 0],
                        [1, 0, 0, 1, 0, 0, 0, 1, 0],
                        [1, 1, 0, 1, 1, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 1, 1, 1, 1],
                        [1, 0, 1, 1, 1, 1, 1, 0, 1],
                        [1, 1, 0, 0, 1, 1, 0, 0, 1],
                        [0, 1, 0, 1, 0, 1, 0, 0, 1],
                        [0, 1, 1, 1, 0, 0, 1, 1, 0],
                        [0, 1, 0, 0, 1, 0, 1, 0, 0]]
    

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

            
    def draw(self):
        pygame.display.set_caption("Sudoku Solver")
        win.fill("white")
    
        for y in range(len(self.testgrid)):
            for x in range(len(self.testgrid[y])):
                # goes through every element of the grid
                pygame.draw.rect(win, self.black, (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 1)
                # draws each elements box
                
                if self.testgridfixed[y][x] == 1:
                    text = self.boldfont.render(str(self.testgrid[y][x]), False, self.black) 
                else:
                    text = self.font.render(str(self.testgrid[y][x]), False, self.black) 
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
        solving = True

        while solving:
            clock.tick(2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    solving = False

            print(self.currentx, self.currenty, self.currentnumber)


            if self.testgridfixed[self.currenty][self.currentx] == 0:

                if self.testgrid[self.currenty][self.currentx] < 9:
                    self.testgrid[self.currenty][self.currentx] += 1
                
                    if(self.checkRow()):
                        
                        if(self.checkColumn()):

                            if(self.checkBox()):
                                #nextbox
                                if self.currentx == 8:
                                    if self.currenty == 8:
                                        print("no solution")
                                        quit()
                                    else:
                                        self.currenty += 1
                                        self.currentx = 0
                                else:
                                    self.currentx += 1

                            else:
                                #increase
                                pass
                        else:
                            #increase
                            pass
                    else:
                        #increase
                        pass

                else:
                    #previous box
                    if self.currentx == 0:
                        self.currenty -= 1
                        self.currentx = 8
                    else:
                        self.currentx -= 1
            
            else:
                pass


            self.draw()

    def checkRow(self):
        self.currentnumber = self.testgrid[self.currenty][self.currentx]
        if self.testgrid[self.currenty].count(self.currentnumber) > 1:
            print("in - row")
            return False
        return True

    def checkColumn(self):
        self.currentnumber = self.testgrid[self.currenty][self.currentx]
        count = 0
        for y in range(len(self.testgrid)):
            if self.currentnumber == self.testgrid[y][self.currentx]:
                count += 1
        if count > 1:
            print("in - column")
            return False
        return True

    def checkBox(self):
        print(self.currenty, self.currentx)
        topleftbox = [0,0]

        topleftbox[0] == self.currentx - (self.currentx % 3)
        topleftbox[1] == self.currenty - (self.currenty % 3)
        count=0

        for i in range(3):
            for j in range(3):
                if self.testgrid[topleftbox[1] + i][topleftbox[0]+j] == self.currentnumber:
                    count += 1

        if count > 1:
            return False
        else:
            return True


        



Sudoku1 = Sudoku()
Sudoku1.solve()
pygame.quit()