import pygame
import SudokuFunctions
import time

start_time = time.time()

pygame.init()
win = pygame.display.set_mode((500,500))

class sudokuInterface():

    def __init__(self):

        self.sudokufunctions = SudokuFunctions.Sudoku()

        self.font = pygame.font.SysFont('Consolas', 25, bold=False)        
        self.boldfont = pygame.font.SysFont('Consolas', 25, bold=True)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)    

        self.origin = [25,25]
        # origin is the top left of the grid, so it can be moved without changing all drawn elements


    def input(self):
        running = True
        while running:
            pygame.display.set_caption("Sudoku Solver")
            win.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousex, mousey = pygame.mouse.get_pos()
                    if self.origin[0] < mousex < 500 - self.origin[0] and self.origin[1] < mousey < 500 - self.origin[1]:
                        xposition = round(mousex / 50) - 1
                        yposition = round(mousey / 50) - 1

                        if self.sudokufunctions.testgrid[yposition][xposition] == 9:
                            self.sudokufunctions.testgrid[yposition][xposition] = 0
                        else:
                            self.sudokufunctions.testgrid[yposition][xposition] += 1
                        

            for y in range(len(self.sudokufunctions.testgrid)):
                for x in range(len(self.sudokufunctions.testgrid[y])):
                    # goes through every element of the grid
                    pygame.draw.rect(win, self.black, (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 1)
                    # draws each elements box
                    if self.sudokufunctions.testgrid[y][x] != 0:
                        text = self.font.render(str(self.sudokufunctions.testgrid[y][x]), False, self.black) 
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
        self.sudokufunctions.dryrun()
        running = True
        while running:
            pygame.display.set_caption("Sudoku Solver")
            win.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.sudokufunctions.solving:
                self.sudokufunctions.solve()
                solving_text = self.font.render("Solving...", False, self.blue)
                solving_text_rect = solving_text.get_rect(center=(pygame.display.get_surface().get_width()/2, pygame.display.get_surface().get_height()/2))
                win.blit(solving_text, solving_text_rect)
            else:
                print("time: %s" %(time.time()-start_time))

                for y in range(len(self.sudokufunctions.testgrid)):
                    for x in range(len(self.sudokufunctions.testgrid[y])):
                        # goes through every element of the grid
                        pygame.draw.rect(win, self.black, (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 1)
                        # draws each elements box
                        if not self.sudokufunctions.solving:
                            text = self.font.render(str(self.sudokufunctions.testgrid[y][x]), False, self.black) 
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