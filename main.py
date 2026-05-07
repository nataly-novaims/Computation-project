from board import Board
from block import Block
from pynput import keyboard
import time

def main():
    # Create the game board
    grid = [
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    ]

    #Create objects
    my_board = Board(grid)

    #Take coordinates of the start position from Class Board and transfer them to Block
    start_row, start_col = my_board.start
    my_block = Block(start_row,start_col)

    print(" WELCOME TO BLOXORZ")
    print("Use the arrow buttons on your keyboard. Press 'Esc' to exit")


    #Showing the board
    my_board.display(block_cells = my_block.get_coordinates())
    while True:

        #Read button press
        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN:
            key =event.name

            #Moving logic
            if key == keyboard.Key.up:
                my_block.move_up()
            elif key == keyboard.Key.down:
                my_block.move_down()
            elif key == keyboard.Key.left:
                my_block.move_left()
            elif key == keyboard.Key.right:
                my_block.move_right()
            elif key == keyboard.Key.esc:
                print("Exit the game")
                break
            else:
                continue #ignore other buttons

            #After move -  check if lost
            new_coords = my_block.get_coordinates()
            alive = True
            for row, col in new_coords:
                if not my_board.is_walkable(row, col):
                    print("Gameover")
                    time.sleep(1)
                    my_block = Block(start_row, start_col) #restart
                    alive = False
                    break


            #Again display board 
            print ("\n" * 5)
            my_board.display(block_cells = my_block.get_coordinates())

            #check if win
            if alive and len(new_coords) == 1:
                row, col = new_coords[0]
                if my_board.is_goal(row, col):
                    print("WIN!!!")
                    break


            time.sleep(0.2)

if __name__ == "__main__":
    main()


