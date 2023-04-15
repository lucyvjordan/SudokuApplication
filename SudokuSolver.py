import pygame

pygame.init()
win = pygame.display.set_mode((500,500))
win.fill("white")


class Sudoku():
    def __init__(self):
        self.grid = [["", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", "", ""],]  
        self.origin = [25,25]

            
    def solve(self):
        solving = True
        while solving:
            pygame.display.set_caption("Sudoku Solver")
        
            for y in range(len(self.grid)):
                for x in range(len(self.grid[y])):
                    pygame.draw.rect(win, "black", (self.origin[0]+(x*50) , self.origin[1]+(y*50), 50, 50), 1)

            for y in range(3):
                for x in range(3):
                    pygame.draw.rect(win, "black", (self.origin[0]+(x*150), self.origin[1]+(y*150), 150, 150), 4)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    solving = False

            pygame.display.update()


Sudoku1 = Sudoku()
Sudoku1.solve()
pygame.quit()