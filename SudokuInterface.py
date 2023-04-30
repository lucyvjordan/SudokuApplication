import pygame
import SudokuFunctions
import time

start_time = time.time()

pygame.init()
win = pygame.display.set_mode((500,550))

class sudokuInterface():

    def __init__(self):

        self.sudokufunctions = SudokuFunctions.Sudoku()

        self.font = pygame.font.SysFont('Consolas', 25, bold=False)
        self.textfont = pygame.font.SysFont('Consolas', 16, bold=True)        
        self.boldfont = pygame.font.SysFont('Consolas', 25, bold=True)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)    

        self.origin = [25,75]
        # origin is the top left of the grid
        # defines this so that the grisd can be moved without manually changing the location of all drawn elements


    def input(self):
        running = True
        valid = True
        while running:
            pygame.display.set_caption("Sudoku Solver")
            win.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    valid = True
                    mousex, mousey = pygame.mouse.get_pos()
                    if self.origin[0] < mousex < self.origin[0] + (9*50) and self.origin[1] < mousey < self.origin[1] + (9*50):
                        xposition = int((mousex - self.origin[0]) / 50)
                        yposition = int((mousey - self.origin[1]) / 50)
                        # finds which box is being clicked
                    
                        if self.sudokufunctions.grid[yposition][xposition] == 9:
                            self.sudokufunctions.grid[yposition][xposition] = 0
                            self.sudokufunctions.gridfixed[yposition][xposition] = 0
                            # if it already contains 9, loop back to the start and make the box empty
                        else:
                            self.sudokufunctions.grid[yposition][xposition] += 1
                            self.sudokufunctions.gridfixed[yposition][xposition] = 1
                            # otherwise increase the box value by 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                valid = self.sudokufunctions.checkGrid()
                if valid:
                    self.draw()

            if not valid:
                invalidtext = self.textfont.render("The values you have entered create an invalid grid.", False, self.black)
                invalidtext_rect = invalidtext.get_rect(center=(pygame.display.get_surface().get_width()/2, 45))
                win.blit(invalidtext, invalidtext_rect) 

            screentext = self.textfont.render("Input your known values, and then press 'S' to solve.", False, self.black)
            screentext_rect = screentext.get_rect(center=(pygame.display.get_surface().get_width()/2, 20))
            win.blit(screentext, screentext_rect)

            for y in range(len(self.sudokufunctions.grid)):
                for x in range(len(self.sudokufunctions.grid[y])):
                    # goes through every element of the grid
                    pygame.draw.rect(win, self.black, (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 1)
                    # draws each elements box
                    if self.sudokufunctions.grid[y][x] != 0:
                        text = self.font.render(str(self.sudokufunctions.grid[y][x]), False, self.black) 
                        # the number will be bold if it is fixed
                        text_rect = text.get_rect(center=(self.origin[0]+25+(x*50) , self.origin[1]+25+(y*50)))
                        win.blit(text, text_rect)
                        # draws each elements number if it is not supposed to be empty

            for y in range(3):
                for x in range(3):
                    pygame.draw.rect(win, self.black, (self.origin[0]+(x*150), self.origin[1]+(y*150), 150, 150), 4)
                    # draws the thicker 3x3 boxes

            pygame.display.update()


    def draw(self):
        solution = self.sudokufunctions.dryrun()

        running = True
        while running:
            pygame.display.set_caption("Sudoku Solver")
            win.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not solution:
                solving_text = self.font.render("No solution", False, self.blue)
                solving_text_rect = solving_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 25))
                win.blit(solving_text, solving_text_rect)
            else:
                if self.sudokufunctions.solving:
                    self.sudokufunctions.solve()
                    solving_text = self.font.render("Solving...", False, self.blue)
                    solving_text_rect = solving_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 25))
                    win.blit(solving_text, solving_text_rect)
                else:
                    solving_text = self.font.render("Solved", False, self.blue)
                    solving_text_rect = solving_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 25))
                    win.blit(solving_text, solving_text_rect)
                    print("time: %s" %(time.time()-start_time))

            for y in range(len(self.sudokufunctions.grid)):
                for x in range(len(self.sudokufunctions.grid[y])):
                    # goes through every element of the grid
                    pygame.draw.rect(win, self.black, (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 1)
                    # draws each elements box
                    if self.sudokufunctions.grid[y][x] != 0:
                        text = self.font.render(str(self.sudokufunctions.grid[y][x]), False, self.black) 
                        # the number will be bold if it is fixed
                        text_rect = text.get_rect(center=(self.origin[0]+25+(x*50) , self.origin[1]+25+(y*50)))
                        win.blit(text, text_rect)
                        # draws each elements number

            for y in range(3):
                for x in range(3):
                    pygame.draw.rect(win, self.black, (self.origin[0]+(x*150), self.origin[1]+(y*150), 150, 150), 4)
                    # draws the thicker 3x3 boxes

            pygame.display.update()

if __name__ == "__main__":
    # this is true when the program starts running
    sudoku = sudokuInterface()
    sudoku.input()
    # keeps the menu running