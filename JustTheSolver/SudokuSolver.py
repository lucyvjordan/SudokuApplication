import pygame
import SudokuFunctions
import time
import sys,os

pygame.init()
win = pygame.display.set_mode((500,600))

class SudokuInterface():

    def __init__(self):
        self.font = pygame.font.SysFont('Consolas', 25, bold=False)
        self.textfont = pygame.font.SysFont('Consolas', 16, bold=True)        
        self.boldfont = pygame.font.SysFont('Consolas', 25, bold=True)
        self.black = (0, 0, 0)
        self.blue = (35, 100, 255)  
        self.white = (255, 255, 255)
        self.backgroundcolour = (50, 151, 194)

        self.origin = [25,125]
        # origin is the top left of the grid
        # defines this so that the grisd can be moved without manually changing the location of all drawn elements

        self.selected = [-1,-1]


    def input(self):
        running = True
        validmessage = ""
        while running:
            pygame.display.set_caption("Sudoku Solver")

            try:
                win.blit(pygame.image.load(os.path.join(sys.path[0],"background.png")), (0,0))
            except:
                win.fill(self.backgroundcolour)
            # so that an error does not occur if the file can't be found or is in the wrong folder

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    validmessage = ""
                    # error message about invalid grid is removed

                    mousex, mousey = pygame.mouse.get_pos()
                    if self.origin[0] < mousex < self.origin[0] + (9*50) and self.origin[1] < mousey < self.origin[1] + (9*50):
                        # if the mouse has been clicked within the grid
                        xposition = int((mousex - self.origin[0]) / 50)
                        yposition = int((mousey - self.origin[1]) / 50)
                        # finds which box is being clicked

                        self.selected = [xposition, yposition]

                        '''if self.sudokufunctions.grid[yposition][xposition] == 9:
                            self.sudokufunctions.grid[yposition][xposition] = 0
                            self.sudokufunctions.gridfixed[yposition][xposition] = 0
                            # if it already contains 9, loop back to the start and make the box empty
                        else:
                            self.sudokufunctions.grid[yposition][xposition] += 1
                            self.sudokufunctions.gridfixed[yposition][xposition] = 1
                            # otherwise increase the box value by 1'''
                        # this was used to input the numbers by clicking on the box, but now numbers are entered with the keyboard
                    else:
                        self.selected = [-1,-1]
                        # unselects whichever box is being entered in

                    
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit() and self.selected != [-1,-1]:  
                        # if key pressed is a number and a box has been selected
                        if int(event.unicode) != 0:
                            # if the number pressed is not 0
                            self.sudokufunctions.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                            self.sudokufunctions.gridfixed[self.selected[1]][self.selected[0]] = 1

            keys = pygame.key.get_pressed()

            if keys[pygame.K_s]:
                validmessage = self.sudokufunctions.checkGrid()
                if validmessage == "":
                    self.selected = [-1,-1]
                    return
            # if 's' is pressed and all the entered values follow sudoku rules, the grid is allowed 

            if keys[pygame.K_BACKSPACE]:
                if self.selected != [-1,-1]:
                    self.sudokufunctions.grid[self.selected[1]][self.selected[0]] = 0
                    self.sudokufunctions.gridfixed[self.selected[1]][self.selected[0]] = 0
            # removes the value from the selected box

            if validmessage != "":
                print("HI")
                if validmessage == "invalid":
                    invalidtext = self.textfont.render("The values you have entered create an invalid grid.", False, self.white)
                else:
                    invalidtext = self.textfont.render("Please enter some values.", False, self.white)
                invalidtext_rect = invalidtext.get_rect(center=(pygame.display.get_surface().get_width()/2, 105))
                win.blit(invalidtext, invalidtext_rect) 
            # if invalid values have been entered, an error message is shown

            screentext = self.textfont.render("Enter your known values, and then press 'S' to solve.", False, self.black)

            self.drawgrid(screentext)

            pygame.display.update()


    def solving(self):
        start_time = time.time()
        solution = self.sudokufunctions.dryrun()

        running = True
        while running:
            pygame.display.set_caption("Sudoku Solver")

            try:
                win.blit(pygame.image.load(os.path.join(sys.path[0],"background.png")), (0,0))
            except:
                win.fill(self.backgroundcolour)
            # so that an error does not occur if the file can't be found or is in the wrong folder


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_c] and not self.sudokufunctions.solving:
                self.resetgrid()

            if not solution:
                self.sudokufunctions.grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
                screen_text = self.textfont.render("No solution. Press 'C' to reset.", False, self.blue)
            # if no solution is found - it has already reset, but this is so that the grid is empty when it shows the 'no solution' message

            else:
                if self.sudokufunctions.solving:
                    self.sudokufunctions.solve()
                    screen_text = self.textfont.render("Solving...", False, self.blue)
                # if the program is in the process of solving the sudoku

                else:
                    screen_text = self.textfont.render("Solution found. Press 'C' to reset.", False, self.blue)
                    print("time: %s" %(time.time()-start_time))
                # if the program has solved the sudoku

            self.drawgrid(screen_text)

            pygame.display.update()
    

    def drawgrid(self, screen_text):

        pygame.draw.rect(win, self.black, (0, 10, 500, 45), 0)

        title_text = self.font.render("- - - - - - - - Sudoku Solver - - - - - - - -", False, self.white)
        title_text_rect = title_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 35))
        win.blit(title_text, title_text_rect)

        for y in range(len(self.sudokufunctions.grid)):
            for x in range(len(self.sudokufunctions.grid[y])):
                # goes through every element of the grid
                box = pygame.draw.rect(win, self.black, (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 0)
                win.fill(self.white, box.inflate(-1, -1))

                # draws each elements box
                if self.sudokufunctions.grid[y][x] != 0:
                    if self.sudokufunctions.grid[y][x] != 0:
                        if self.sudokufunctions.gridfixed[y][x] == 1:
                            text = self.boldfont.render(str(self.sudokufunctions.grid[y][x]), False, self.black)
                        else:
                            text = self.font.render(str(self.sudokufunctions.grid[y][x]), False, self.black)
                        # the number will be bold if it is fixed
                    text_rect = text.get_rect(center=(self.origin[0]+25+(x*50) , self.origin[1]+25+(y*50)))
                    win.blit(text, text_rect)
                    # draws each elements number if it is not supposed to be empty

        for y in range(3):
            for x in range(3):
                pygame.draw.rect(win, self.black, (self.origin[0]+(x*150), self.origin[1]+(y*150), 150, 150), 4)
                # draws the thicker 3x3 boxes

        if self.selected != [-1,-1]:
            box = pygame.draw.rect(win, self.blue, (self.origin[0]+(self.selected[0]*50) , self.origin[1]+(self.selected[1]*50), 50, 50), 3)
        # draws a green box around the selected box

        pygame.draw.rect(win, self.white, (0, 59, 500, 30), 0)
        screen_text_rect = screen_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 75))
        win.blit(screen_text, screen_text_rect)


    def resetgrid(self):
        # resets the grid to empty
        self.sudokufunctions = SudokuFunctions.Sudoku()
        sudoku.input()
        sudoku.solving()


if __name__ == "__main__":
    # this is true when the program starts running
    sudoku = SudokuInterface()
    sudoku.resetgrid()
    # keeps the menu running
