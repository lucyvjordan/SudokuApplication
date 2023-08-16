import pygame
import sys, os

pygame.init()

win = pygame.display.set_mode((500, 600))


def start_menu():
    
    backgroundcolour = (50, 151, 194)
    font = pygame.font.SysFont('Consolas', 25, bold=False)
    textfont = pygame.font.SysFont('Consolas', 20, bold=True)        
    boldfont = pygame.font.SysFont('Consolas', 25, bold=True)
    black = (0, 0, 0)
    blue = (35, 100, 255)  
    white = (255, 255, 255)    
    difficulty = ["EASY", "MEDIUM", "HARD"]

    while True:

        x = 0
        y = 0
        pressing = False

        pygame.display.set_caption("Sudoku Start Menu")

        try:
            win.blit(pygame.image.load(os.path.join(sys.path[0],"background.png")), (0,0))
        except:
            win.fill(backgroundcolour)
        # so that an error does not occur if the file can't be found or is in the wrong folder

        pygame.draw.rect(win, white, (0, 10, 500, 45))

        title_text = font.render("Sudoku Start Menu", False, backgroundcolour)
        title_text_rect = title_text.get_rect(center=(pygame.display.get_surface().get_width()/2, 35))
        win.blit(title_text, title_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressing = True
                x,y = event.pos
                print("CLICK")

        for i in range(1, 4):

            borderRect = pygame.Rect(0, 0, 200, 75)
            borderRect.center = (pygame.display.get_surface().get_width()/2, i*120)
            pygame.draw.rect(win, white, borderRect)

            innerRect = pygame.Rect(0, 0, 195, 70)
            innerRect.center = borderRect.center
            pygame.draw.rect(win, backgroundcolour, innerRect)

            difficulty_text = textfont.render(difficulty[i-1],False, white)
            difficulty_text_rect = difficulty_text.get_rect(center=innerRect.center)
            win.blit(difficulty_text, difficulty_text_rect)

            if innerRect.collidepoint(x,y) and pressing:
                return difficulty[i-1]

        solverRect = pygame.draw.rect(win, white, (5, 450, 490, 75))
        innersolverRect = pygame.draw.rect(win, black, (7.5, 452.5, 485, 70))
    
        solver_text = textfont.render("OR... solve a sudoku you're stuck on!", False, white)
        solver_text_rect = solver_text.get_rect(center=innersolverRect.center)
        win.blit(solver_text, solver_text_rect)

        if innersolverRect.collidepoint(x,y) and pressing:
            print("user trying to solve sudoku - still need to code")

        pygame.display.update()
