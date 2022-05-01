# Name: Gun, Warwick
# Date: 22/01/2022
# Description: GUI for the user

# Importing libraries
import pygame, sys  # https://www.pygame.org/docs/
from SudokuBoard import Sudoku_board
import datetime  # https://docs.python.org/3/library/datetime.html
import copy  # https://docs.python.org/3/library/copy.html

pygame.init()  # Initializing pygame
screen = pygame.display.set_mode((495, 640))
clock = pygame.time.Clock()

# Globals
state = 'main'  # Variable to keep track of the state
game_status = "not_done"

selected_index = 0  # Variable to keep track of the index
R, G, B = 127.5, 127.5, 127.5  # Keep track of RGB values
customizable = {
    "1": (127.5, 127.5, 127.5),
    "2": (127.5, 127.5, 127.5),
    "3": (127.5, 127.5, 127.5),
    "4": (127.5, 127.5, 127.5),
    "5": (127.5, 127.5, 127.5),
    "6": (127.5, 127.5, 127.5),
    "7": (127.5, 127.5, 127.5),
    "8": (127.5, 127.5, 127.5),
    "9": (127.5, 127.5, 127.5),
    "around": (226, 231, 237),
    "selected": (187, 222, 251),
    "background": (255, 255, 255),
    "fixed": (0, 0, 0),
    "border": (180, 179, 177)
}
selected_squares = []  # Keeps track of what are the squares that needs to be highlighed

# OFFSETS
Y_OFFSET = 55

# Music Initialization
# pygame.mixer.music.load('music.mp3')
# pygame.mixer.music.play(-1)

# Font Initialization
pygame.font.init()
number_font = pygame.font.SysFont("dejavuserif", 20, False, False)
customizable_font = pygame.font.SysFont("dejavuserif", 100, False, False)

# Initializing a board 
board = Sudoku_board()
shown = board.calculate_shown("two")
original = copy.deepcopy(shown)

# Timer Setup
timer = 00.00
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Amount of player's life
lives = 3

# Initialize images
silver = pygame.image.load("silver.png")
silver = pygame.transform.scale(silver, (300, 300))

gold = pygame.image.load("gold.png")
gold = pygame.transform.scale(gold, (300, 300))

platinum = pygame.image.load("platinum.png")
platinum = pygame.transform.scale(platinum, (300, 300))

logo = pygame.image.load("logo.jpg")
logo = pygame.transform.scale(logo, (300, 100))

# Variables for correct / incorrect count
correct = 0
incorret = 0

selected = (0, 0)  # Keeping track of the selected square


# Inputs is a screen, position of the mouse click
# Returns the top left corner of the square that needs to the clicked
def update_selected(screen, position):
    # Checks if the mouse button is even in the grid
    if position[1] <= 9 * 55 + Y_OFFSET - 1 and position[1] > Y_OFFSET:
        x = position[0] - (position[0] % 55)
        y = position[1] - (position[1] % 55 + Y_OFFSET)
        return (x, y)

    return (selected[0], selected[1])


# Function to display what medal the user had won
# Input is only the screen and the output is automatically drawn onto the screen
def display_winner(screen):
    if timer < 120:
        screen.blit(platinum, (100, 150))

    elif timer < 300:
        screen.blit(gold, (100, 150))

    else:
        screen.blit(silver, (100, 150))


def draw_selected_squares(screen):
    squares = []
    # Drawing the selected squares
    for i in range(9):
        for j in range(9):
            if i * 55 == selected[1] and j * 55 != selected[0]:
                pygame.draw.rect(screen, customizable["around"], [j * 55, i * 55 + Y_OFFSET, 55, 55])
                squares.append((i, j))

            elif j * 55 == selected[0] and i * 55 != selected[1]:
                pygame.draw.rect(screen, customizable["around"], [j * 55, i * 55 + Y_OFFSET, 55, 55])
                squares.append((i, j))

    box_x = int(selected[0] / 55 / 3)
    box_y = int(selected[1] / 55 / 3)

    for k in range(3):
        for l in range(3):
            pygame.draw.rect(screen, customizable["around"],
                             [((box_x * 3) + l) * 55, ((box_y * 3) + k) * 55 + Y_OFFSET, 55, 55])
            squares.append((((box_y * 3) + k), ((box_x * 3) + l)))

    pygame.draw.rect(screen, customizable["selected"], [selected[0] + 2, selected[1] + 2 + Y_OFFSET, 51, 51])
    return squares


def restart(difficulty):
    print(f"Updated to {difficulty} difficulty")
    global lives, board, shown, selected, state, original, timer, game_status
    state = "play"
    lives = 3
    timer = 00.00
    board = Sudoku_board()
    shown = board.calculate_shown(difficulty)
    original = copy.deepcopy(shown)
    selected = (0, 0)
    game_status = "not_done"


# Game loop
while True:
    if state == "main":  # In the main state
        state = 'main'
        screen.fill((0, 0, 0))

        screen.blit(logo, (100, 150))
        header = number_font.render("SUDOKU", True, (255, 255, 255))
        screen.blit(header, (100, 130))

        play_button = pygame.Rect(197.5, 300, 100, 30)
        pygame.draw.rect(screen, (255, 255, 255), play_button)
        screen.blit(number_font.render("PLAY", True, (0, 0, 0)), (222.5, 300))

        theme_button = pygame.Rect(197.5, 340, 100, 30)
        pygame.draw.rect(screen, (255, 255, 255), theme_button)
        screen.blit(number_font.render("THEME", True, (0, 0, 0)), (207, 340))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                if play_button.collidepoint(pygame.mouse.get_pos()):
                    state = 'play'

                elif theme_button.collidepoint(pygame.mouse.get_pos()):
                    state = 'theme'

    elif state == "theme":  # Theme state
        screen.fill((0, 0, 0))

        # Drawing the close button
        close_button = pygame.Rect(435, 0, 60, 30)
        pygame.draw.rect(screen, (255, 0, 0), (435, 0, 60, 30))
        screen.blit(number_font.render("X", True, (0, 0, 0)), (460, 0))

        # Drawing the left button
        left_button = pygame.Rect(50, 300, 50, 30)
        pygame.draw.rect(screen, (255, 255, 255), left_button)

        right_button = pygame.Rect(150, 300, 50, 30)
        pygame.draw.rect(screen, (120, 120, 120), right_button)

        # Drawing the rgb sliders
        red_rgb = pygame.Rect(300, 100, 100, 20)
        pygame.draw.rect(screen, (255, 255, 255), red_rgb)
        pygame.draw.rect(screen, (0, 0, 0), (R + 300, 100, 10, 20))

        green_rgb = pygame.Rect(300, 200, 100, 20)
        pygame.draw.rect(screen, (255, 255, 255), green_rgb)
        pygame.draw.rect(screen, (0, 0, 0), (G + 300, 200, 10, 20))

        blue_rgb = pygame.Rect(300, 300, 100, 20)
        pygame.draw.rect(screen, (255, 255, 255), blue_rgb)
        pygame.draw.rect(screen, (0, 0, 0), (B + 300, 300, 10, 20))

        # Drawing the theme buttons
        sand_theme = pygame.Rect(395, 0, 30, 30)
        pygame.draw.rect(screen, (242, 234, 219), sand_theme)

        black_theme = pygame.Rect(360, 0, 30, 30)
        pygame.draw.rect(screen, (62, 61, 71), black_theme)

        white_theme = pygame.Rect(325, 0, 30, 30)
        pygame.draw.rect(screen, (255, 255, 255), white_theme)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                if close_button.collidepoint(pygame.mouse.get_pos()):
                    state = 'main'

                elif left_button.collidepoint(pygame.mouse.get_pos()):
                    if selected_index == 0:
                        selected_index = len(customizable) - 6
                    else:
                        selected_index -= 1
                    R, G, B = customizable[list(customizable.keys())[selected_index]]

                elif right_button.collidepoint(pygame.mouse.get_pos()):
                    if selected_index == len(customizable) - 6:
                        selected_index = 0
                    else:
                        selected_index += 1
                    R, G, B = customizable[list(customizable.keys())[selected_index]]

                elif red_rgb.collidepoint(pygame.mouse.get_pos()):
                    R = pygame.mouse.get_pos()[0] - 300

                elif green_rgb.collidepoint(pygame.mouse.get_pos()):
                    G = pygame.mouse.get_pos()[0] - 300

                elif blue_rgb.collidepoint(pygame.mouse.get_pos()):
                    B = pygame.mouse.get_pos()[0] - 300

                elif sand_theme.collidepoint(pygame.mouse.get_pos()):  # Color scheme taken from "Sudoku" app
                    customizable["background"] = (242, 234, 219)
                    customizable["around"] = (232, 220, 196)
                    customizable["fixed"] = (88, 79, 71)
                    customizable["border"] = (180, 179, 177)
                    customizable["selected"] = (187, 222, 251)

                elif black_theme.collidepoint(pygame.mouse.get_pos()):  # Color scheme taken from "Sudoku" app
                    customizable["background"] = (37, 36, 44)
                    customizable["around"] = (29, 29, 37)
                    customizable["fixed"] = (117, 116, 121)
                    customizable["border"] = (62, 61, 71)
                    customizable["selected"] = (136, 165, 189)

                elif white_theme.collidepoint(pygame.mouse.get_pos()):  # Color scheme taken from "Sudoku" app
                    customizable["background"] = (255, 255, 255)
                    customizable["around"] = (226, 231, 237)
                    customizable["fixed"] = (0, 0, 0)
                    customizable["border"] = (180, 179, 177)
                    customizable["selected"] = (187, 222, 251)

        customizable[list(customizable.keys())[selected_index]] = (R, G, B)

        pygame.draw.rect(screen, customizable["around"], (50, 100, 200, 200))
        number = customizable_font.render(str(selected_index + 1), True, customizable[str(selected_index + 1)])
        screen.blit(number, (75, 125))
        pygame.draw.rect(screen, (255, 255, 255), (50, 100, 200, 200), 2)

    elif state == "play":
        if lives == 0:
            print("All lifes lost")
            restart("easy")
        state = 'play'
        timer_ticked = False
        screen.fill((customizable["around"]))

        # Drawing the close button
        close_button = pygame.Rect(435, 0, 60, 30)
        pygame.draw.rect(screen, (255, 0, 0), (435, 0, 60, 30))
        screen.blit(number_font.render("X", True, (0, 0, 0)), (460, 0))

        # Drawing the difficulty buttons
        if game_status != "won":
            easy_difficulty = pygame.Rect(172.5, 610, 50, 30)
            pygame.draw.rect(screen, (150, 255, 152), easy_difficulty)

            medium_difficulty = pygame.Rect(247.5, 610, 50, 30)
            pygame.draw.rect(screen, (255, 242, 143), medium_difficulty)

            hard_difficulty = pygame.Rect(322.5, 610, 50, 30)
            pygame.draw.rect(screen, (189, 126, 126), hard_difficulty)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                sys.exit()

            elif event.type == pygame.USEREVENT:
                if not board.solved(shown) and not timer_ticked:
                    timer_ticked = True
                    timer += 1

            elif event.type == pygame.MOUSEBUTTONUP:
                if game_status == "won":
                    again = pygame.Rect(197.5, 500, 100, 40)
                    if again.collidepoint(pygame.mouse.get_pos()):
                        restart("easy")

                else:
                    if easy_difficulty.collidepoint(pygame.mouse.get_pos()):
                        restart("easy")

                    elif medium_difficulty.collidepoint(pygame.mouse.get_pos()):
                        restart("medium")

                    elif hard_difficulty.collidepoint(pygame.mouse.get_pos()):
                        restart("hard")

                    elif close_button.collidepoint(pygame.mouse.get_pos()):
                        state = "main"

                selected = update_selected(screen, pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                if str(event.unicode).isnumeric():

                    if int(event.unicode) != 0:
                        previous = shown[int(selected[1] / 55)][int(selected[0] / 55)]

                        if board.valid(int(event.unicode), (int(selected[0] / 55), int(selected[1] / 55)), shown):
                            shown[int(selected[1] / 55)][int(selected[0] / 55)] = str(event.unicode)

                            if not board.box_valid(shown):
                                shown[int(selected[1] / 55)][int(selected[0] / 55)] = previous
                                lives -= 1

                        else:
                            lives -= 1
                            shown[int(selected[1] / 55)][int(selected[0] / 55)] = previous
                elif event.key == pygame.K_BACKSPACE:
                    if original[int(selected[1] / 55)][int(selected[0] / 55)] == 0:
                        shown[int(selected[1] / 55)][int(selected[0] / 55)] = 0
                    else:
                        print("Cannot Delete; It was part of the original squares.")

        if board.solved(shown) and board.box_valid(shown):
            display_winner(screen)
            text = number_font.render("Play Again", True, customizable["fixed"])
            again = pygame.Rect(197.5, 500, 100, 40)
            pygame.draw.rect(screen, customizable["background"], again)
            game_status = "won"
            pygame.display.update()
            continue

        # Drawing the selected squares
        selected_squares = draw_selected_squares(screen)

        # Drawing the grid
        y = 0 + Y_OFFSET
        for i in range(9):
            x = 0
            for j in range(9):
                if (i, j) not in selected_squares:
                    pygame.draw.rect(screen, (customizable["background"]), ([x, y, 55, 55]))
                pygame.draw.rect(screen, customizable["border"], [x, y, 55, 55], 2)
                if original[i][j] != 0:
                    number = number_font.render(str(shown[i][j]), True, customizable["fixed"])
                    screen.blit(number, (x + 20, y + 27.5))
                elif shown[i][j] != 0:
                    number = number_font.render(str(shown[i][j]), True, customizable[str(shown[i][j])])
                    screen.blit(number, (x + 20, y + 27.5))

                x += 55
            y += 55

        y = 0 + Y_OFFSET
        for i in range(3):
            x = 0

            for j in range(3):
                pygame.draw.rect(screen, (0, 0, 0), [x, y, 165, 165], 2)
                x += 165

            y += 165

        # Drawing the bottom half
        text = number_font.render(str(datetime.timedelta(seconds=timer)), True, customizable["fixed"])
        screen.blit(text, (0, 30))

        life = number_font.render(f"Lives: {str(lives)}", True, customizable["fixed"])
        screen.blit(life, (0, 620))

    clock.tick(60)
    pygame.display.update()
