import pygame
import Sudoku_Functions
import Start_Menu
import time
import datetime
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
        self.playing = True

        undo_sprite = pygame.image.load(os.path.join(sys.path[0],"sprites/undo_sprite.png"))
        restart_sprite = pygame.image.load(os.path.join(sys.path[0],"sprites/restart_sprite.png"))
        check_sprite = pygame.image.load(os.path.join(sys.path[0],"sprites/check_sprite.png"))        
        quit_sprite = pygame.image.load(os.path.join(sys.path[0],"sprites/quit_sprite.png"))

        self.icons = [undo_sprite, restart_sprite, check_sprite, quit_sprite]
        self.icons_X = [284, 332, 380, 428]

        self.previousmoves = []

    def inputting(self):
        running = True
        self.startTime = time.time()

        while running:
            pygame.display.set_caption("Sudoku")

            try:
                win.blit(pygame.image.load(os.path.join(sys.path[0],"sprites/background.png")), (0,0))
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

                        if self.icons_X[0] < mousex < self.icons_X[-1] + 40:
                            if 60 < mousey < 100:
                                for i in range(len(self.icons_X)):
                                    if self.icons_X[i] < mousex < self.icons_X[i] + 40:
                                        
                                        if i == 0:
                                            #undo
                                            if len(self.previousmoves) != 0:
                                                self.sudokufunctions.grid[self.previousmoves[-1][0]][self.previousmoves[-1][1]] = self.previousmoves[-1][2]
                                                # set the value at the index directed in the stack to the number also contained in the stack

                                                if self.previousmoves[-1][2] == 0:
                                                    # if removing a number from the grid, set its fixed value to 0
                                                    self.sudokufunctions.gridfixed[self.previousmoves[-1][0]][self.previousmoves[-1][1]] == 0
                                                else:
                                                    # if adding a number to the grid, set its fixed value to 2
                                                    self.sudokufunctions.gridfixed[self.previousmoves[-1][0]][self.previousmoves[-1][1]] == 2

                                                self.previousmoves.pop()
                                                # remove the move from the stack

                                        elif i == 1:
                                            # restart
                                            for y in range(9):
                                                for x in range(9):
                                                    if self.sudokufunctions.gridfixed[y][x] == 2:
                                                        # then the number has been entered by the user
                                                        self.sudokufunctions.gridfixed[y][x] = 0
                                                        self.sudokufunctions.grid[y][x] = 0
                                            self.previousmoves = []

                                        elif i == 2:
                                            # check - still to code
                                            if self.sudokufunctions.grid == self.sudokufunctions.completegrid:
                                                self.solved = True
                                                self.selected = [-1, -1]
                                                print("correct")
                                            else:
                                                print("incorrect")

                                        else:
                                            # quit
                                            difficulty = Start_Menu.start_menu()
                                            sudoku.resetgrid(difficulty)
                                            
                if event.type == pygame.KEYDOWN and self.solved == False:             
                    if event.unicode.isdigit() and self.selected != [-1,-1]:
                        # if key pressed is a number and a box has been selected
                        self.solutiontext = ""
                        if int(event.unicode) != 0:
                            # if the number pressed is not 0
                            print(self.previousmoves)
                            if self.sudokufunctions.grid[self.selected[1]][self.selected[0]] != int(event.unicode):
                                # only changes value if it is different to value already in the box
                                self.previousmoves.append([self.selected[1], self.selected[0], self.sudokufunctions.grid[self.selected[1]][self.selected[0]]])
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

            # BACKSPACE
            if keys[pygame.K_BACKSPACE] and self.solved == False:
                if self.selected != [-1,-1] and self.sudokufunctions.grid[self.selected[1]][self.selected[0]] != 0:

                    self.previousmoves.append([self.selected[1], self.selected[0], self.sudokufunctions.grid[self.selected[1]][self.selected[0]]])
                    # add the removal to the previous moves

                    self.sudokufunctions.grid[self.selected[1]][self.selected[0]] = 0
                    self.sudokufunctions.gridfixed[self.selected[1]][self.selected[0]] = 0
                    # removes the value from the selected box


            self.drawgrid()

            pygame.display.update()


    def drawgrid(self):

        pygame.draw.rect(win, self.black, (0, 10, 500, 45), 0)

        title_text = self.font.render("- - - - - - - - Sudoku - - - - - - - -", False, self.white)
        title_text_rect = title_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 35))
        win.blit(title_text, title_text_rect)

        # BOXES AND NUMBERS
        for y in range(len(self.sudokufunctions.grid)):
            for x in range(len(self.sudokufunctions.grid[y])):
                # goes through every element of the grid
                box = pygame.draw.rect(win, self.black, (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 0)
                win.fill(self.white, box.inflate(-1, -1))

                # draws each elements box
                if self.sudokufunctions.grid[y][x] != 0:
                    if self.sudokufunctions.gridfixed[y][x] == 1:
                        text = self.boldfont.render(str(self.sudokufunctions.grid[y][x]), False, self.black)
                        # the number will be bold as it is fixed
                    else:
                        text = self.font.render(str(self.sudokufunctions.grid[y][x]), False, self.blue)
                    text_rect = text.get_rect(center=(self.origin[0]+25+(x*50) , self.origin[1]+25+(y*50)))
                    win.blit(text, text_rect)
                    # draws each elements number if it is not supposed to be empty

        # THICKER 3X3 BOXES
        for y in range(3):
            for x in range(3):
                pygame.draw.rect(win, self.black, (self.origin[0]+(x*150), self.origin[1]+(y*150), 150, 150), 4)

        # GREEN BOX AROUND SELECTED BOX
        if self.selected != [-1,-1]:
            box = pygame.draw.rect(win, self.blue, (self.origin[0]+(self.selected[0]*50) , self.origin[1]+(self.selected[1]*50), 50, 50), 3)

        # INFORMATION TAB
        timeSection = pygame.draw.rect(win, self.white, (self.origin[0], 60, 250, 40), 0)
        iconsSection = pygame.draw.rect(win, self.blue, (self.origin[0] + 250, 60, 200, 40), 0)

        # TIME TAKEN
        currentTime = time.time() - self.startTime

        if currentTime > 60 * 60 * 24 and self.playing:
            currentTime = datetime.timedelta(seconds=round(time.time() - self.startTime)).days
            # if over a day, display the number of days only
        
            if currentTime > 1:
                self.screentext = self.font.render(f"Time: {str(currentTime)} days", True, self.black)
            else:
                self.screentext = self.font.render(f"Time: {str(currentTime)} day", True, self.black)

        else:
            currentTime = datetime.timedelta(seconds=round(time.time() - self.startTime))
            self.screentext = self.font.render(f"Time: {str(currentTime)}", True, self.black)
            # display the time in hours:minutes:seconds format

        screentext_rect = self.screentext.get_rect(center=(timeSection.center))        

        win.blit(self.screentext, screentext_rect)

        # GAME ICONS
        for i in range(len(self.icons)):
            win.blit(self.icons[i], (self.icons_X[i], 60))


    def resetgrid(self, difficulty):
        # resets the grid to empty
        self.sudokufunctions = Sudoku_Functions.SudokuFunctions()
        self.sudokufunctions.difficulty = difficulty
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