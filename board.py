from colorama import Fore, Style, init
from constants import *


init(autoreset=True)
 
# cell values:
# 0 = empty, 1 = normal, 2 = start, 3 = fragile, 4 = teleport, 9 = goal
 
class Board:
 
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start = self.find_tile(2)   #find where block starts
        self.goal = self.find_tile(9)    #find the goal
 
    def find_tile(self, value):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == value:
                    return (row, col)
        raise ValueError("Tile " + str(value) + " not found on board.")
 
    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
 
    def is_walkable(self, row, col):
        #cell is walkable if its inside the grid and not empty
        return self.in_bounds(row, col) and self.grid[row][col] != 0
 
    def is_goal(self, row, col):
        return (row, col) == self.goal
 
    def get_cell(self, row, col):
        if not self.in_bounds(row, col):
            return 0
        return self.grid[row][col]
 
    def display(self, block_cells=None):
        if block_cells is None:
            block_cells = []
 
        occupied = set(block_cells)
 
        #column numbers on top
        print("   " + "".join(str(col % 10) for col in range(self.cols)))
        print("   " + "-" * self.cols)
 
        for row in range(self.rows):
            row_str = str(row).rjust(2) + "|"
            for col in range(self.cols):
                pos = (row, col)
                cell = self.grid[row][col]
 
                if pos in occupied:
                    
                    row_str += Fore.CYAN + Style.BRIGHT + "B" + Style.RESET_ALL   #block
                elif cell == 0:
                    row_str += Fore.BLACK + Style.BRIGHT + "_" + Style.RESET_ALL  #empty
                elif cell == 9:
                    row_str += Fore.GREEN + Style.BRIGHT + "G" + Style.RESET_ALL  #goal
                elif cell == 2:
                    row_str += Fore.YELLOW + Style.BRIGHT + "S" + Style.RESET_ALL #start
                elif cell == 3:
                    row_str += Fore.RED + "F" + Style.RESET_ALL                   #fragile
                elif cell == 4:
                    row_str += Fore.MAGENTA + Style.BRIGHT + "T" + Style.RESET_ALL #teleport
                else:
                    row_str += Fore.WHITE + "." + Style.RESET_ALL                 #normal tile
 
            print(row_str)
        print()