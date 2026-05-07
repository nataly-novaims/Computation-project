"""
board.py - Board class for the Bloxorz puzzle game.

Cell values:
    0 = Empty cell  (block falls here)
    1 = Normal tile (safe)
    2 = Start tile  (where block begins)
    9 = Goal tile   (where block must finish)
"""

class Board:
    """Represents the Bloxorz game board as a 2D grid."""

    def __init__(self, grid):
        """
        Load the board from a 2D list of integers.

        Args:
            grid: 2D list of integers representing the board.
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start = self.find_tile(2)   # find where the block starts
        self.goal  = self.find_tile(9)   # find the goal position 

    def find_tile(self, value):
        """
        Search the grid and return (row, col) of the given tile value.

        Args:
            value: The tile integer to look for (2 or 9).

        Returns:
            (row, col) tuple of the tile's position.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == value:
                    return (row, col)
        raise ValueError(f"Tile {value} not found on the board.")

    def in_bounds(self, row, col):
        """
        Check if (row, col) is inside the grid.

        Returns:
            True if the position is within the grid boundaries.
        """
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_walkable(self, row, col):
        """
        Check if the block can safely land on (row, col).
        A cell is walkable if it is in bounds AND not empty (not 0).

        Returns:
            True if safe to step on, False if the block would fall.
        """
        return self.in_bounds(row, col) and self.grid[row][col] != 0

    def is_goal(self, row, col):
        """
        Check if (row, col) is the goal tile.

        Returns:
            True if this is the goal position.
        """ 
        return (row, col) == self.goal

    def display(self, block_cells=None):
        """
        Print the board in the console.

        Symbols:
            B = block is here
            G = goal tile
            S = start tile
            . = normal tile
            _ = empty gap

        Args:
            block_cells: list of (row, col) positions the block occupies.
        """
        if block_cells is None:
            block_cells = []

        occupied = set(block_cells)

        # print column numbers across the top
        print("   " + "".join(str(col % 10) for col in range(self.cols)))
        print("   " + "-" * self.cols)

        for row in range(self.rows):
            row_str = f"{row:2d}|"
            for col in range(self.cols):
                pos = (row, col)
                cell = self.grid[row][col]

                if pos in occupied:
                    row_str += "B"          # block is here
                elif cell == 0:
                    row_str += "_"          # empty gap
                elif cell == 9:
                    row_str += "G"          # goal
                elif cell == 2:
                    row_str += "S"          # start
                else:
                    row_str += "."          # normal tile

            print(row_str)
        print()


# -------------------------------------------------------
# Test it — run: python board.py
# -------------------------------------------------------
if __name__ == "__main__":
    # Example board from the project spec (Listing 1)
    grid = [
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    ]

    board = Board(grid)

    print(f"Start position : {board.start}")   # (1, 1)
    print(f"Goal  position : {board.goal}")    # (4, 7)
    print(f"Grid size      : {board.rows} rows x {board.cols} cols")
    print()

    print("Board (no block):")
    board.display()

    print("Board (block standing at start):")
    board.display(block_cells=[board.start])

    print("Board (block lying flat — occupying two cells):")
    board.display(block_cells=[(1, 1), (1, 2)])

    # Quick checks
    print(f"Is (1,1) walkable? {board.is_walkable(1, 1)}")   # True
    print(f"Is (0,3) walkable? {board.is_walkable(0, 3)}")   # False (empty)
    print(f"Is (4,7) the goal? {board.is_goal(4, 7)}")       # True
    print(f"Is (-1,0) in bounds? {board.in_bounds(-1, 0)}")  # False
