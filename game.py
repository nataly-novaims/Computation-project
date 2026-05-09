from board import Board
from block import Block
from solver import bfs, astar
from levels import Levels, Teleports, choose_level
from colorama import Fore, Style, init
from pynput import keyboard
import time
import threading
 
init(autoreset=True)
 
level_order = ["1", "2", "3", "4", "5", "6"]
 
# this variable stores the last key pressed
# we use threading because pynput Listener runs in background
last_key = None
key_ready = threading.Event()
 
 
def on_press(key):
    global last_key
    try:
        last_key = key.char  # normal keys like 'u'
    except AttributeError:
        last_key = key       # special keys like Key.up, Key.esc
    key_ready.set()
 
 
def wait_for_key():
    # wait until a key is pressed then return it
    key_ready.clear()
    key_ready.wait()
    return last_key
 
 
def check_special_tiles(my_block, my_board, level_key):
    #check if block landed on a special tile after moving
    coords = my_block.get_coordinates()
    my_block.get_orientation()
 
    if my_block.orientation == "Standing":
        row, col = coords[0]
 
        #fragile tile - block cant stand upright on it
        if my_board.get_cell(row, col) == 3:
            return "fell"
 
        #teleport tile - move block to linked position
        if my_board.get_cell(row, col) == 4:
            tmap = Teleports.get(level_key, {})
            if (row, col) in tmap:
                dest_row, dest_col = tmap[(row, col)]
                my_block.row1 = dest_row
                my_block.col1 = dest_col
                my_block.row2 = dest_row
                my_block.col2 = dest_col
                return "teleported"
 
    return "ok"
 
 
def run_solver(my_board, start_row, start_col):
    print()
    print("Which algorithm do you want to use?")
    print("  " + Fore.YELLOW + "1" + Style.RESET_ALL + " - BFS  (finds shortest solution)")
    print("  " + Fore.YELLOW + "2" + Style.RESET_ALL + " - A*   (uses distance to goal, usually faster)")
    print()
    algo = input("Enter 1 or 2: ").strip()
    print()
 
    if algo == "2":
        print(Fore.MAGENTA + "Running A*..." + Style.RESET_ALL)
        t_start = time.time()
        solution = astar(my_board, start_row, start_col)
        t_end = time.time()
        name = "A*"
    else:
        print(Fore.MAGENTA + "Running BFS..." + Style.RESET_ALL)
        t_start = time.time()
        solution = bfs(my_board, start_row, start_col)
        t_end = time.time()
        name = "BFS"
 
    print()
 
    if solution is None:
        print(Fore.RED + "No solution found." + Style.RESET_ALL)
        return
 
    elapsed = round((t_end - t_start) * 1000, 2)
 
    print(Fore.GREEN + "------------------------------" + Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT + name + " finished!" + Style.RESET_ALL)
    print("Total moves : " + Fore.YELLOW + str(len(solution)) + Style.RESET_ALL)
    print("Time taken  : " + Fore.YELLOW + str(elapsed) + " ms" + Style.RESET_ALL)
    print("Solution    : " + Fore.CYAN + " -> ".join(solution) + Style.RESET_ALL)
    print(Fore.GREEN + "------------------------------" + Style.RESET_ALL)
    print()
    input("Press Enter to watch the solution step by step...")
    print()
 
    #replay solution on the board step by step
    replay = Block(start_row, start_col)
    print("Starting position:")
    my_board.display(block_cells=replay.get_coordinates())
 
    step = 1
    for move in solution:
        time.sleep(0.7)
 
        if move == "up":
            replay.move_up()
        elif move == "down":
            replay.move_down()
        elif move == "left":
            replay.move_left()
        elif move == "right":
            replay.move_right()
 
        print(Fore.CYAN + "Step " + str(step) + " of " + str(len(solution)) + Style.RESET_ALL + "  ->  " + Fore.YELLOW + Style.BRIGHT + move.upper() + Style.RESET_ALL)
        my_board.display(block_cells=replay.get_coordinates())
        step = step + 1
 
    print(Fore.GREEN + Style.BRIGHT + "Solver completed the level!" + Style.RESET_ALL)
 
 
def play_level(level_key, grid):
    #create board and block objects
    my_board = Board(grid)
    start_row, start_col = my_board.start
    my_block = Block(start_row, start_col)
    move_count = 0
 
    print()
    print(Fore.CYAN + Style.BRIGHT + "=== Level " + level_key + " ===" + Style.RESET_ALL)
    print()
    print("Legend: " +
          Fore.CYAN + "B" + Style.RESET_ALL + "=block  " +
          Fore.GREEN + "G" + Style.RESET_ALL + "=goal  " +
          Fore.YELLOW + "S" + Style.RESET_ALL + "=start  " +
          Fore.RED + "F" + Style.RESET_ALL + "=fragile  " +
          Fore.MAGENTA + "T" + Style.RESET_ALL + "=teleport")
    print()
 
    #ask player to choose mode
    print("What do you want to do?")
    print("  " + Fore.YELLOW + "1" + Style.RESET_ALL + " - Play manually")
    print("  " + Fore.YELLOW + "2" + Style.RESET_ALL + " - Solve automatically")
    print()
    mode = input("Enter 1 or 2: ").strip()
    print()
 
    #solver mode
    if mode == "2":
        run_solver(my_board, start_row, start_col)
        return ask_after_level(level_key)
 
    #manual mode
    print("Arrow keys to move. Press U to undo last move. Press Esc to quit.")
    print()
    my_board.display(block_cells=my_block.get_coordinates())
 
    history = []  #saves previous positions for undo
 
    # start keyboard listener in background
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
 
    while True:
        key = wait_for_key()
 
        if key == keyboard.Key.esc:
            listener.stop()
            print("Exiting...")
            return "exit"
 
        #undo last move
        if key == "u":
            if len(history) == 0:
                print("Nothing to undo.")
            else:
                last_r1, last_c1, last_r2, last_c2 = history.pop()
                my_block.row1 = last_r1
                my_block.col1 = last_c1
                my_block.row2 = last_r2
                my_block.col2 = last_c2
                move_count = move_count - 1
                print(Fore.YELLOW + "Move undone." + Style.RESET_ALL)
                print()
                my_board.display(block_cells=my_block.get_coordinates())
            continue
 
        if key not in (keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right):
            continue  #ignore other keys
 
        #save state before moving (used for undo)
        history.append((my_block.row1, my_block.col1, my_block.row2, my_block.col2))
 
        #move the block
        if key == keyboard.Key.up:
            my_block.move_up()
        elif key == keyboard.Key.down:
            my_block.move_down()
        elif key == keyboard.Key.left:
            my_block.move_left()
        elif key == keyboard.Key.right:
            my_block.move_right()
 
        move_count = move_count + 1
        new_coords = my_block.get_coordinates()
        alive = True
 
        #check if block fell off the board
        for row, col in new_coords:
            if not my_board.is_walkable(row, col):
                print("\n" * 3)
                my_board.display(block_cells=new_coords)
                print(Fore.RED + "Block fell! Restarting level..." + Style.RESET_ALL)
                time.sleep(1)
                my_block = Block(start_row, start_col)
                move_count = 0
                history = []
                alive = False
                break
 
        if alive:
            #check special tiles
            result = check_special_tiles(my_block, my_board, level_key)
 
            if result == "fell":
                print("\n" * 3)
                my_board.display(block_cells=my_block.get_coordinates())
                print(Fore.RED + "Block fell through fragile tile! Restarting..." + Style.RESET_ALL)
                time.sleep(1)
                my_block = Block(start_row, start_col)
                move_count = 0
                history = []
                alive = False
 
            elif result == "teleported":
                print(Fore.MAGENTA + "Teleported!" + Style.RESET_ALL)
 
        #show board and move count
        print("\n" * 3)
        print("Moves: " + Fore.YELLOW + str(move_count) + Style.RESET_ALL)
        my_board.display(block_cells=my_block.get_coordinates())
 
        #check if won
        if alive and len(new_coords) == 1:
            row, col = new_coords[0]
            if my_board.is_goal(row, col):
                listener.stop()
                print(Fore.GREEN + Style.BRIGHT + "YOU WIN! Completed in " + str(move_count) + " moves!" + Style.RESET_ALL)
                time.sleep(1)
                return ask_after_level(level_key)
 
        time.sleep(0.15)
 
 
def ask_after_level(level_key):
    print()
    print("What do you want to do next?")
    print("  " + Fore.YELLOW + "1" + Style.RESET_ALL + " - Replay this level")
    print("  " + Fore.YELLOW + "2" + Style.RESET_ALL + " - Next level")
    print("  " + Fore.YELLOW + "3" + Style.RESET_ALL + " - Choose a different level")
    print("  " + Fore.YELLOW + "4" + Style.RESET_ALL + " - Exit")
    print()
    choice = input("Enter choice: ").strip()
 
    if choice == "1":
        return "replay"
    elif choice == "2":
        return "next"
    elif choice == "3":
        return "choose"
    else:
        return "exit"
 
 
def main():
    print(Fore.CYAN + Style.BRIGHT + "==============================")
    print(Fore.CYAN + Style.BRIGHT + "      WELCOME TO BLOXORZ")
    print(Fore.CYAN + Style.BRIGHT + "==============================")
    print()
 
    level_key = choose_level()
 
    while True:
        grid = Levels.get(level_key)
 
        if grid is None:
            print("Level not found.")
            break
 
        result = play_level(level_key, grid)
 
        if result == "exit":
            print(Fore.CYAN + "Thanks for playing!" + Style.RESET_ALL)
            break
 
        elif result == "replay":
            continue
 
        elif result == "next":
            if level_key in level_order:
                current_index = level_order.index(level_key)
                if current_index + 1 < len(level_order):
                    level_key = level_order[current_index + 1]
                else:
                    print(Fore.GREEN + Style.BRIGHT + "You completed all levels! Well done!" + Style.RESET_ALL)
                    break
            else:
                print("No next level.")
                break
 
        elif result == "choose":
            level_key = choose_level()
 
 
if __name__ == "__main__":
    main()