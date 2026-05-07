class Block:

    def __init__(self, start_row, start_col):
        #first part of the block
        self.row1 = start_row
        self. col1 = start_col

        #second part of the block
        self.row2 = start_row
        self.col2 = start_col

    def get_coordinates(self):
        #get coordinates
        if self.row1 == self.row2 and self.col1 == self.col2:
            return [(self.row1, self.col1)]
        else:
            return [(self.row1, self.col1),(self.row2, self.col2)]

    def get_orientation(self):
        #define orientation
        if self.row1 == self.row2 and self.col1 == self.col2:
            self.orientation = "Standing"
        elif self.row1 == self.row2 :
            self.orientation = "Horizontal"
        else:
            self.orientation = "Vertical"
        return self.orientation

    def move_right(self):
        #if we move to right
        self.get_orientation()
        if self.orientation == "Standing":
            self.row1 = self.row1
            self.col1 = self.col1 + 1
            self.row2 = self.row2
            self.col2 = self.col2 + 2
            self.orientation = "Horizontal"
        elif self.orientation == "Horizontal":
            new_col = self.col2 + 1
            self.col1 = new_col
            self.col2 = new_col
            self.orientation = "Standing"
        else:
            self.row1 = self.row1
            self.col1 = self.col1 + 1
            self.row2 = self.row2
            self.col2 = self.col2 + 1
            self.orientation = "Vertical"
        self.get_orientation()

    def move_left(self):
        #if we move to left
        self.get_orientation()
        if self.orientation == "Standing":
            self.row1 = self.row1
            self.col1 = self.col1 - 1
            self.row2 = self.row2
            self.col2 = self.col2 - 2
            self.orientation = "Horizontal"
        elif self.orientation == "Horizontal":
            new_col = self.col1 - 1
            self.col1 = new_col
            self.col2 = new_col
            self.orientation = "Standing"
        else:
            self.row1 = self.row1
            self.col1 = self.col1 - 1
            self.row2 = self.row2
            self.col2 = self.col2 - 1
            self.orientation = "Vertical"
        self.get_orientation()
        
    def move_up(self):
        #if we move up
        self.get_orientation()
        if self.orientation == "Standing":
            self.row1 = self.row1 - 2
            self.col1 = self.col1 
            self.row2 = self.row2 - 1
            self.col2 = self.col2 
            self.orientation = "Vertical"
        elif self.orientation == "Horizontal":
            self.row1 = self.row1 - 1
            self.col1 = self.col1
            self.row2 = self.row2 - 1
            self.col2 = self.col2
            self.orientation = "Horizontal"
        else:
            self.row1 = self.row1 - 1
            self.col1 = self.col1
            self.row2 = self.row1 - 1
            self.col2 = self.col2
            self.orientation = "Standing"
        self.get_orientation()

    def move_down(self):
         #if we move down
        self.get_orientation()
        if self.orientation == "Standing":
            self.row1 = self.row1 + 1
            self.col1 = self.col1 
            self.row2 = self.row2 + 2
            self.col2 = self.col2 
            self.orientation = "Vertical"
        elif self.orientation == "Horizontal":
            self.row1 = self.row1 + 1
            self.col1 = self.col1
            self.row2 = self.row2 + 1
            self.col2 = self.col2
            self.orientation = "Horizontal"
        else:
            self.row1 = self.row2 + 1
            self.col1 = self.col1
            self.row2 = self.row2 + 1
            self.col2 = self.col2
            self.orientation = "Standing"
        self.get_orientation()

