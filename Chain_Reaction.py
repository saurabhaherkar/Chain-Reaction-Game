import pygame
from pygame.locals import *
from tkinter import *
from tkinter import messagebox
import random

# Initialization
pygame.init()

# Screen Size
display_width = display_height = 600

# Grid Size
rows = columns = 6

# Cell Size
y_cell_size = int(display_height / rows)
x_cell_size = int(display_width / columns)
# columns ==> x
# rows ==> y

# Show Screen
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Chain Reaction - Jigar Gajjar')

# For Animation
fps_clock = pygame.time.Clock()

# Players Turn Variable
turn = 1


def toggle_turn():
    global turn
    turn = 0 if turn == 1 else 1


def next_turn():
    # Do not change turn variable's value
    # Just return next players turn
    return 0 if turn == 1 else 1


class Color:
    shade = [(244, 67, 54), (0, 163, 232)]  # shade[0] ==> Player 1,  shade[1] ==> Player2
    BLACK = (0, 0, 0)


class Cell:
    def __init__(self):
        self.color = None  # Color of current cell
        self.atoms = 0  # Number of atoms in the cell
        self.neighbors = []  # Neighbors of this cell

    def add_neighbors(self, x_index, y_index):
        # Merged the observations, we can write multiple if statements like y_index == 0  and x_index == 0 etc
        if y_index > 0:
            self.neighbors.append(ChainReaction.grid[x_index][y_index - 1])
        if y_index < rows - 1:
            self.neighbors.append(ChainReaction.grid[x_index][y_index + 1])
        if x_index > 0:
            self.neighbors.append(ChainReaction.grid[x_index - 1][y_index])
        if x_index < columns - 1:
            self.neighbors.append(ChainReaction.grid[x_index + 1][y_index])


class ChainReaction:
    grid = []

    def __init__(self):
        # Make 2D Array for grid having Cell object in it
        for x in range(columns):
            grid_row = []
            for y in range(rows):
                grid_row.append(Cell())
            ChainReaction.grid.append(grid_row)

    @staticmethod
    def make(line_color):
        # Clear Screen
        screen.fill(Color.BLACK)
        # Draw Vertical Lines
        for i in range(columns):
            pygame.draw.line(screen, line_color, (i * x_cell_size, 0), (i * x_cell_size, y_cell_size * columns), 1)
        # Draw Horizontal Lines
        for i in range(rows):
            pygame.draw.line(screen, line_color, (0, i * y_cell_size), (x_cell_size * rows, i * y_cell_size), 1)

    @staticmethod
    def wobble(position):
        xrandom = random.randint(1, 2) * random.choice([-1, 1])  # [1,2] * [1,-1]
        yrandom = random.randint(1, 2) * random.choice([-1, 1])  # [1,2] * [1,-1]
        position = (position[0] + xrandom, position[1] + yrandom)
        return position

    @staticmethod
    def draw_atoms():
        # Iterate through grid array and display number of atoms
        for y in range(rows):
            for x in range(columns):
                if ChainReaction.grid[y][x].color:

                    color = ChainReaction.grid[y][x].color
                    radius = int(x_cell_size * 0.1)  # 10 % of cell size

                    x_center = x * x_cell_size + int(x_cell_size / 2)  # X coordinate of center of Cell
                    y_center = y * y_cell_size + int(y_cell_size / 2)  # Y coordinate of Center of Cell

                    if ChainReaction.grid[y][x].atoms == 1:  # if number of atoms = 1, make 1 filled circle
                        position = ChainReaction.wobble((x_center, y_center))
                        pygame.draw.circle(screen, color, position, radius)  # Circle 1
                    elif ChainReaction.grid[y][x].atoms == 2:  # if number of atoms = 2, make 2 filled circles
                        position = ChainReaction.wobble((x_center - int(x_cell_size * 0.1), y_center))
                        pygame.draw.circle(screen, color, position, radius)  # Circle 1

                        position = ChainReaction.wobble((x_center + int(x_cell_size * 0.1), y_center))
                        pygame.draw.circle(screen, color, position, radius)  # Circle 2
                    elif ChainReaction.grid[y][x].atoms == 3:  # if number of atoms = 3, make 3 filled circles
                        position = ChainReaction.wobble(
                            (x_center - int(x_cell_size * 0.1), y_center - int(x_cell_size / 1.2 * 0.1)))
                        pygame.draw.circle(screen, color, position, radius)  # Circle 1

                        position = ChainReaction.wobble(
                            (x_center + int(x_cell_size * 0.1), y_center - int(x_cell_size / 1.2 * 0.1)))
                        pygame.draw.circle(screen, color, position, radius)  # Circle 2

                        position = ChainReaction.wobble((x_center, y_center + int(x_cell_size / 1.2 * 0.1)))
                        pygame.draw.circle(screen, color, position, radius)  # Circle 3

    @staticmethod
    def burst(cell):
        cell.atoms = 0  # Make current cell empty
        cell.color = None  # Make current cell's color blank

        # Increment neighbor's value on burst
        for neighbor in cell.neighbors:
            neighbor.atoms = neighbor.atoms + 1
            neighbor.color = Color.shade[turn]  # Conquer neighbor color
        for neighbor in cell.neighbors:
            if neighbor.atoms > 3:  # Recursive Burst
                ChainReaction.burst(neighbor)

    @staticmethod
    def check_winner():
        player1_score = 0
        player2_score = 0
        for y in range(rows):
            for x in range(columns):
                if ChainReaction.grid[y][x].color:
                    # Check cell color with current players color and count
                    if ChainReaction.grid[y][x].color == Color.shade[turn]:
                        player1_score = player1_score + 1
                    else:
                        player2_score = player2_score + 1

        # >=2 to check if it is not the start of the game
        if player1_score >= 2 and player2_score == 0:
            return turn
        elif player2_score >= 2 and player1_score == 0:
            return next_turn()
        else:
            return -1

    @staticmethod
    def add_atom(position):
        x = position[0]
        y = position[1]
        # Normalize any point to index values
        x_index = int((x - (x - x_cell_size * int(x / x_cell_size))) / x_cell_size)
        y_index = int((y - (y - y_cell_size * int(y / y_cell_size))) / y_cell_size)

        # Return if clicked on other players cell
        if ChainReaction.grid[y_index][x_index].color == Color.shade[next_turn()]:
            return

        # Else Add atom to the cell
        ChainReaction.grid[y_index][x_index].atoms = ChainReaction.grid[y_index][x_index].atoms + 1
        ChainReaction.grid[y_index][x_index].color = Color.shade[turn]

        # If there are no neighbors then add neighbors
        if not ChainReaction.grid[y_index][x_index].neighbors:
            ChainReaction.grid[y_index][x_index].add_neighbors(y_index, x_index)

        # Condition to burst
        if ChainReaction.grid[y_index][x_index].atoms > 3:
            ChainReaction.burst(ChainReaction.grid[y_index][x_index])

        # After adding atom it is now other player's turn
        toggle_turn()

        # ReDraw the addition of atoms and burst results
        ChainReaction.make(Color.shade[turn])
        ChainReaction.draw_atoms()


def event_handler():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
            pygame.quit()
            quit()
        elif event.type == MOUSEBUTTONUP:
            ChainReaction.add_atom(pygame.mouse.get_pos())


if __name__ == '__main__':
    ChainReaction().make(Color.shade[turn])
    while True:
        fps_clock.tick(30)
        event_handler()
        pygame.display.update()
        result = ChainReaction.check_winner()
        if result == -1:  # Game is still on!!!
            ChainReaction.make(Color.shade[turn])
            ChainReaction.draw_atoms()
            continue
        else:
            Tk().wm_withdraw()  # To hide the main window
            player = 'BLUE' if turn == 0 else 'RED'
            messagebox.showinfo('Game Over', 'Player {} Wins'.format(player))
            break