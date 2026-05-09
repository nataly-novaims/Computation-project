# all levels stored here
# 0=empty, 1=normal, 2=start, 3=fragile, 4=teleport, 9=goal
 
Levels = {
 
    "1": [
        [1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 2, 1, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 9, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 0]
    ],
 
    "2": [
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [2, 1, 1, 0, 0, 1, 1, 9, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
    ],
 
    "3": [
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [2, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 9, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0]
    ],
 
    #level 4 has fragile tiles (3) - block cant stand upright on them
    "4": [
        [0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0],
        [0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [1, 2, 1, 0, 0, 1, 1, 1, 1, 3, 3, 3, 3, 3],
        [1, 1, 1, 0, 0, 1, 1, 1, 1, 3, 3, 3, 3, 3],
        [0, 0, 0, 0, 0, 1, 9, 1, 0, 0, 3, 3, 1, 3],
        [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 3, 3, 3, 3]
    ],
 
    #level 5 has teleport tiles (4)
    "5": [
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 2, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 1, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    ],
 
    "6": [
        [0, 0, 0, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 0, 1, 1, 2],
        [1, 0, 1, 1, 1, 9, 1, 1],
        [0, 1, 0, 0, 1, 1, 1, 0]
    ]
}
 
# teleport pairs for each level
# when block stands on a teleport tile it moves to the linked tile
Teleports = {
    "5": {(1, 6): (3, 8), (3, 8): (1, 6)}
}
 
 
def choose_level():
    choice = input("Choose level (1-6) or press C to create your own: ").strip().lower()
 
    if choice in {"1", "2", "3", "4", "5", "6"}:
        return choice
    elif choice == "c":
        create_level()
        return "custom"
    else:
        print("Invalid choice, try again.")
        return choose_level()
 
 
def create_level():
    base_cells = {0, 1, 2, 9}
    extra_cells = {3, 4}
 
    print()
    print("Welcome to level creation mode!")
    print("Cell types: 0=empty  1=normal  2=start  3=fragile  4=teleport  9=goal")
    print()
 
    rows = 0
    cols = 0
    while rows < 4 or cols < 4:
        print("Minimum size is 4x4.")
        rows = int(input("Number of rows: "))
        cols = int(input("Number of columns: "))
 
    while True:
        new_level = []
        used_base = set()
 
        for i in range(rows):
            row = []
            for j in range(cols):
                while True:
                    cell = input("Cell (" + str(i) + ", " + str(j) + "): ")
                    if cell.isdigit() and int(cell) in base_cells:
                        number = int(cell)
                        row.append(number)
                        used_base.add(number)
                        break
                    elif cell.isdigit() and int(cell) in extra_cells:
                        row.append(int(cell))
                        break
                    else:
                        print("Invalid. Use 0, 1, 2, 3, 4 or 9.")
            new_level.append(row)
 
        #check all base tiles were placed at least once
        if used_base == base_cells:
            print("Level created successfully!")
            break
        else:
            print("You must use 0, 1, 2 and 9 at least once. Try again.")
 
    Levels["custom"] = new_level