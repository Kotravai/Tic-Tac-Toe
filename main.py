import pygame
import time
import numpy as np

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
WIDTH = 100
HEIGHT = 100
MARGIN = 10
X = pygame.image.load("x.png")
O = pygame.image.load("o.png")
grid = []
click = 0

# Creating a 3 X 3 Matrix
for row in range(3):
    grid.append([])
    for column in range(3):
        grid[row].append(0)

pygame.init()
window_size = [500, 400]
scr = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tic-Tac-Toe")
done = False
clock = pygame.time.Clock()

# checking if the game is over and identifying the winning line
def winner(grid):
    board = np.array(grid)
    for player in range(1, 3):
        mask = board == player
        out = mask.all(0).any() | mask.all(1).any()
        out2 = np.diag(mask).all() | np.diag(mask[:, ::-1]).all()
        if out:
            if mask.all(0).any():
                return player, f"c{np.where(mask.all(0))[0][0]}"
            elif mask.all(1).any():
                return player, f"r{np.where(mask.all(1))[0][0]}"
        elif out2:
            if np.diag(mask).all():
                return player, "d1"
            elif np.diag(mask[:, ::-1]).all():
                return player, "d2"


# Display message at end of the game
def game_end(text):
    text_font = pygame.font.Font('freesansbold.ttf', 50)
    text_surface = text_font.render(text, True, blue)
    text_rect = text_surface.get_rect()
    text_rect.center = ((window_size[0]/2), (window_size[1]/2))
    scr.blit(text_surface, text_rect)
    pygame.display.update()


# Main Game Loop

while not done:
    # Get coordinates where you click.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            try:
                if grid[row][column] == 0:
                    click += 1
                    if click % 2 == 1:
                        grid[row][column] = 1
                    else:
                        grid[row][column] = 2
                print("Click ", pos, "Grid coordinates: ", row, column)
            except IndexError:
                pass

# Drawing the rectangles
        scr.fill(black)
        for row in range(3):
            for column in range(3):
                pygame.draw.rect(scr,
                                 white,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
# Marking Xs and Os
                if click != 0:
                    if grid[row][column] == 1:
                        x_coord = column * (MARGIN + WIDTH) + WIDTH / 4
                        y_coord = row * (MARGIN + HEIGHT) + HEIGHT / 4
                        scr.blit(X, (x_coord, y_coord))
                    elif grid[row][column] == 2:
                        x_coord = column * (MARGIN + WIDTH) + WIDTH / 4
                        y_coord = row * (MARGIN + HEIGHT) + HEIGHT / 4
                        scr.blit(O, (x_coord, y_coord))


# Game status Check
        if click >= 9:
            game_end("The Game is a tie")
            pygame.display.flip()
            time.sleep(4)
            done = True

        elif 10 > click > 4:
            try:
                won_by = winner(grid)[0]
                win_strike = winner(grid)[1]

            except TypeError:
                break

            if won_by == 1 or won_by == 2:
                if win_strike == 'd1':
                    strike_line = pygame.draw.line(scr, blue, (50, 50), (270, 270), width=4)
                elif win_strike == 'd2':
                    strike_line = pygame.draw.line(scr, blue, (270, 50), (50, 270), width=4)
                elif win_strike[0] == 'r':
                    row_num = int(win_strike[1])
                    row_width = row_num * (MARGIN + WIDTH) + WIDTH / 2
                    strike_line = pygame.draw.line(scr, blue, (50, row_width), (270, row_width), width=4)
                elif win_strike[0] == 'c':
                    col_num = int(win_strike[1])
                    col_width = col_num * (MARGIN + HEIGHT) + HEIGHT / 2
                    strike_line = pygame.draw.line(scr, blue, (col_width, 50), (col_width, 270), width=4)

                game_end(f"Player {won_by} wins")
                pygame.display.flip()
                time.sleep(4)
                done = True

    clock.tick(150)
    pygame.display.flip()
pygame.quit()

