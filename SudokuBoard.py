# Name: Gun, Warwick 
# Date: 1/21/2022
# Description: Make a sudoku game and possibly a sudoku ai

import random
# Constants
SIZE = 9

class Sudoku_board:
  def __init__(self):
    self.size = SIZE

  # My Partner, Warwick, made this function
  # Loops through a 2 dimensional grid and returns a list of all the empty space ie. 0
  def available_space(self, grid):
    avail = []
    for i in range(self.size):
        for j in range(self.size):
          if grid[i][j] == 0:
            avail.append(tuple([j, i]))
    return avail
  
  # Position will be passed in as a tuple (x, y) coords
  def valid(self, number, position, grid):
    # Checks horizontally
    for i in range(self.size):
      if grid[position[1]][i] == number and i != position[0]:
        # print("Horizontally")
        return False
    
    # Checks vertically
    for i in range(self.size):
      if grid[i][position[0]] == number and i != position[1]:
        # print("vertically")
        return False
    
    
    return True

  # Input is an empty 2 dimensional list
  # Output is a 2 dimensional list with numbers or False if it couldnt generate a board
  def generate_board(self, grid):
    print("Generating Board...")
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    random.shuffle(numbers)
    test_grid = grid.copy()

    # Checks if the grid is solved
    if self.solved(test_grid):
      return test_grid
    
    # Loops through all of the available_space
    for position in self.available_space(test_grid):
      # Loops trough each number
      for number in numbers:
        
        # Checks if it is valid
        if self.valid(number, position, test_grid):
          test_grid[position[1]][position[0]] = number

          if self.box_valid(test_grid):
            if self.generate_board(test_grid): # If it is valid, then call another layer else reset it back to 0
              test_grid[position[1]][position[0]] = number
              return test_grid

            else:
              test_grid[position[1]][position[0]] = 0

          else:
            test_grid[position[1]][position[0]] = 0

      return False
    

  def box_valid(self, grid):
    for column in range(3):
      for horizontal in range(3):
        numbers = []
        for y in range(3):
          for x in range(3):

            if grid[y + (column * 3)][x + (horizontal * 3)] not in numbers:

              if grid[y + (column * 3)][x + (horizontal * 3)] != 0:
                numbers.append(grid[y + (column * 3)][x + (horizontal * 3)])

            else:
              return False
        
    return True


  def output(self, grid):
    for row in grid:
      print(row)

    print()

  def solved(self, grid):
    for y in range(self.size):
      numbers = []
      for x in range(self.size):

        if grid[y][x] in numbers or grid[y][x] == 0:
          return False

        else:
          numbers.append(grid[y][x])
    
    # Checks vertically
    for x in range(self.size):
      numbers = []

      for y in range(self.size):

        if grid[y][x] in numbers or grid[y][x] == 0:
          return False

        else:
          numbers.append(grid[y][x])

    return True
  
  # Input is 1 difficulty and output is a grid
  def calculate_shown(self, difficulty):
    # See how many squares we need to remove based on the difficulty passed in
    
    # "Testing" and "one" are for debugging purposed
    if difficulty == "testing":
      amount = 0

    elif difficulty == "one":
      amount = 1

    elif difficulty == "two":
      amount = 2

    elif difficulty == "easy":
      amount = 15

    elif difficulty == "medium":
      amount = 20

    elif difficulty == "hard":
      amount = 30

    # Starts making a grid
    grid = []
    for i in range(self.size):
      grid.append([0] * self.size)

    # Generates the cells 
    grid = self.generate_board(grid)
    print(f"Successfully generated {difficulty} board")
    
    random_cells = []
    while len(random_cells) < amount:
      y = random.randint(0,SIZE - 1)
      x = random.randint(0,SIZE - 1)

      if (x, y) not in random_cells:
        random_cells.append((x, y))
        grid[y][x] = 0

    return grid


  
