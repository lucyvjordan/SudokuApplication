import pygame
import Sudoku_Functions
import Start_Menu
import time
import sys,os

pygame.init()
win = pygame.display.set_mode((500,600))

class Sudoku():

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
        self.solutiontext = ""


    def inputting(self):
        running = True

        while running:
            pygame.display.set_caption("Sudoku")

            try:
                win.blit(pygame.image.load(os.path.join(sys.path[0],"background.png")), (0,0))
            except:
                win.fill(self.backgroundcolour)
            # so that an error does not occur if the file can't be found or is in the wrong folder

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and self.solved == False:

                        mousex, mousey = pygame.mouse.get_pos()
                        if self.origin[0] < mousex < self.origin[0] + (9*50) and self.origin[1] < mousey < self.origin[1] + (9*50):
                            # if the mouse has been clicked within the grid
                            xposition = int((mousex - self.origin[0]) / 50)
                            yposition = int((mousey - self.origin[1]) / 50)
                            # finds which box is being clicked

                            if self.sudokufunctions.gridfixed[yposition][xposition] == 1:
                                # player will only be able to select boxes which do not contain fixed points
                                self.selected = [-1, -1]
                            else:
                                self.selected = [xposition, yposition]

                        else:
                            self.selected = [-1,-1]
                            # unselects whichever box is being entered in
                            
                if event.type == pygame.KEYDOWN and self.solved == False:             
                    if event.unicode.isdigit() and self.selected != [-1,-1]:
                        # if key pressed is a number and a box has been selected
                        self.solutiontext = ""
                        if int(event.unicode) != 0:
                            # if the number pressed is not 0
                            self.sudokufunctions.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                            self.sudokufunctions.gridfixed[self.selected[1]][self.selected[0]] = 2
                            # the grid fixed is set to 2 so it is still recognised as a fixed point if in future I want the player to be able to solve the rest of sudokus they cant finish, but will not be rendered blue like fixed point '1's are
                        
                        movingtonext = True
                        while movingtonext:
                            if self.selected != [8,8]:
                                # this if statement will move the player automatically to the next box when they enter a number
                                if self.selected[0] == 8:
                                    self.selected = [0, self.selected[1] + 1]
                                else:
                                    self.selected = [self.selected[0] + 1, self.selected[1]]
                            else:
                                self.selected = [0,0]

                            if self.sudokufunctions.gridfixed[self.selected[1]][self.selected[0]] == 1:
                                # if the next box is a fixed digit, then keeping going onto the next box
                                pass
                            else:
                                movingtonext = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_g]:
                self.resetgrid(self.sudokufunctions.difficulty)

            if keys[pygame.K_BACKSPACE] and self.solved == False:
                if self.selected != [-1,-1]:
                    self.sudokufunctions.grid[self.selected[1]][self.selected[0]] = 0
                    self.sudokufunctions.gridfixed[self.selected[1]][self.selected[0]] = 0
            # removes the value from the selected box

            if keys[pygame.K_s]:
                # solve
                if self.sudokufunctions.grid == self.sudokufunctions.completegrid:
                    self.solutiontext = self.textfont.render("Correct solution. Press G to generate a new grid.", False, self.black)
                    self.solved = True
                    self.selected = [-1, -1]
                else:
                    self.solutiontext = self.textfont.render("Incorrect solution.", False, self.black)
            
            self.screentext = self.textfont.render("Check solution: S", False, self.black)

            if self.solutiontext == "":
                self.drawgrid()
            else:
                self.drawgrid()

            pygame.display.update()


    def drawgrid(self):

        pygame.draw.rect(win, self.black, (0, 10, 500, 45), 0)

        title_text = self.font.render("- - - - - - - - Sudoku - - - - - - - -", False, self.white)
        title_text_rect = title_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 35))
        win.blit(title_text, title_text_rect)

        for y in range(len(self.sudokufunctions.grid)):
            for x in range(len(self.sudokufunctions.grid[y])):
                # goes through every element of the grid
                box = pygame.draw.rect(win, self.black, (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 0)
                win.fill(self.white, box.inflate(-1, -1))

                # draws each elements box
                if self.sudokufunctions.grid[y][x] != 0:
                    if self.sudokufunctions.gridfixed[y][x] == 1:
                        text = self.boldfont.render(str(self.sudokufunctions.grid[y][x]), False, self.blue)
                        # the number will be bold as it is fixed
                    else:
                        text = self.boldfont.render(str(self.sudokufunctions.grid[y][x]), False, self.black)
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


        optionsLeftHalf = pygame.draw.rect(win, self.white, (0, 59, 250, 30), 0)
        optionsRightHalf = pygame.draw.rect(win, self.blue, (250, 59, 250, 30), 0)
        
        if self.solutiontext == "":
            screentext_rect = self.screentext.get_rect(center=(optionsLeftHalf.center))
            win.blit(self.screentext, screentext_rect)
        else:
            solutiontext_rect = self.solutiontext.get_rect(center=(optionsLeftHalf.center))
            win.blit(self.solutiontext, solutiontext_rect)


    def resetgrid(self, difficulty):
        # resets the grid to empty
        self.sudokufunctions = Sudoku_Functions.SudokuFunctions()
        self.sudokufunctions.difficulty = difficulty
        self.solutiontext = ""
        self.solved = False
        self.sudokufunctions.Generate()
        self.inputting()
        #sudoku.inputting()


if __name__ == "__main__":
    # this is true when the program starts running
    sudoku = Sudoku()
    sudoku.sudokufunctions = Sudoku_Functions.SudokuFunctions()
    difficulty = Start_Menu.start_menu()
    sudoku.resetgrid(difficulty)
    # keeps the menu running