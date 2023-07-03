import pygame
import SudokuGeneratorPART2
import time
import sys,os

pygame.init()
win = pygame.display.set_mode((500,600))

class sudokuInterface():

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
        while running:
            pygame.display.set_caption("Sudoku Generator")

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

            if keys[pygame.K_g]:
                self.sudokugenerator.Generate()

            screentext = self.textfont.render("Press G to generate a grid.", False, self.black)

            self.drawgrid(screentext)

            pygame.display.update()


    def generating(self):
        start_time = time.time()

        running = True
        while running:
            pygame.display.set_caption("Sudoku Generator")

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
            
            if keys[pygame.K_g]:
                screen_text = self.textfont.render("Generating...", False, self.blue)
                self.resetgrid()
                self.sudokugenerator.Generate()

            if keys[pygame.K_c] and not self.sudokugenerator.generating:
                self.resetgrid()

            if self.sudokugenerator.generating:
                screen_text = self.textfont.render("Generating...", False, self.blue)
            # if the program is in the process of solving the sudoku

            else:
                screen_text = self.textfont.render("Press G to generate a grid.", False, self.black)
            # if the program has solved the sudoku

            self.drawgrid(screen_text)

            pygame.display.update()
    

    def drawgrid(self, screen_text):

        pygame.draw.rect(win, self.black, (0, 10, 500, 45), 0)

        title_text = self.font.render("- - - - - - - - Sudoku Generator - - - - - - - -", False, self.white)
        title_text_rect = title_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 35))
        win.blit(title_text, title_text_rect)

        for y in range(len(self.sudokugenerator.grid)):
            for x in range(len(self.sudokugenerator.grid[y])):
                # goes through every element of the grid
                box = pygame.draw.rect(win, self.black, (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 0)
                win.fill(self.white, box.inflate(-1, -1))

                # draws each elements box
                if self.sudokugenerator.grid[y][x] != 0:
                    if self.sudokugenerator.grid[y][x] != 0:
                        text = self.boldfont.render(str(self.sudokugenerator.grid[y][x]), False, self.black)
                        # the number will be bold as it is fixed
                    text_rect = text.get_rect(center=(self.origin[0]+25+(x*50) , self.origin[1]+25+(y*50)))
                    win.blit(text, text_rect)
                    # draws each elements number if it is not supposed to be empty

        for y in range(3):
            for x in range(3):
                pygame.draw.rect(win, self.black, (self.origin[0]+(x*150), self.origin[1]+(y*150), 150, 150), 4)
                # draws the thicker 3x3 boxes


        pygame.draw.rect(win, self.white, (0, 59, 500, 30), 0)
        screen_text_rect = screen_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 75))
        win.blit(screen_text, screen_text_rect)


    def resetgrid(self):
        # resets the grid to empty
        self.sudokugenerator = SudokuGeneratorPART2.SudokuGenerator()
        #sudoku.input()


if __name__ == "__main__":
    # this is true when the program starts running
    sudoku = sudokuInterface()
    sudoku.resetgrid()
    sudoku.generating()
    # keeps the menu running