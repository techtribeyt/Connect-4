# imported libraries
import keyboard
import pyautogui
import mouse
import time
import webbrowser

# classes & functions we defined
from connect4 import Connect4
from mcts import ucb2_agent

# press this button to start the game
# since the program waits until it sees a grid,
# you can press it before the grid appears on the screen
start_button = 'p'

# start the program
keyboard.wait(start_button)

def get_grid_coords(grid):
    # get coordinates of the centers of 42 squares in the game
    xs = [int(grid.left + grid.width // 14 + i * grid.width // 7) for i in range(7)]
    ys = [int(grid.top + grid.height // 12 + i * grid.height // 6) for i in range(6)]

    coords = []
    for y in ys:
        row = []
        for x in xs:
            row.append((x, y))
        coords.append(row)
    return coords

def turn_first(grid, coords):
    # figure out turn and colors
    mouse.move(coords[3][3][0], coords[3][3][1])
    time.sleep(0.1)
    mid_x = (coords[3][3][0] + coords[4][3][0]) // 2
    mid_y = (coords[3][3][1] + coords[4][3][1]) // 2
    pixel = pyautogui.pixel(mid_x, mid_y)
    
    # why? Column is highlighted in dark gray if its your turn
    # so if its light gray, computer goes second
    light_gray = pix_equal(pixel, (206, 212, 218))  
    return not light_gray

# easily compare pixel RGB values
def pix_equal(pixel, goal):
    return pixel[0] == goal[0] and pixel[1] == goal[1] and pixel[2] == goal[2]

# update 2d list board (since now we store everything in bit strings in the Position object)
def board_move(board, loc, turn):
    for i in range(len(board)-1, -1, -1):
        if board[i][loc] == 0:
            board[i][loc] = 1 if turn == 0 else 2
            break


def run(grid):    
     # find 6x7 grid and coords of all squares
     coords = get_grid_coords(grid)
     
          
     # initialize game
     pos = Connect4().get_initial_position()
     board = [[0 for _ in range(7)] for _ in range(6)]
     
     
     # figure out turns
     first_player = turn_first(grid, coords)

     # define strategy (seconds per move as argument)
     strategy = ucb2_agent(7)

     while not pos.terminal:
        # computer's turn
        if (first_player and pos.turn == 0) or (not first_player and pos.turn == 1):
            # computer computes best move
            move = strategy(pos)
            
            # move and click mouse to make move on physical game
            mouse.move(coords[0][move][0], coords[0][move][1])
            mouse.click()
            
            # update 2d board & position object
            board_move(board, move, pos.turn)
            pos = pos.move(move)
        # player's turn
        else:
             # continuously check whether opponent has made a move
             found_move = False
             for i in range(len(coords)):
                 for j in range(len(coords[0])):
                     if found_move: continue
                     pix = pyautogui.pixel(coords[i][j][0], coords[i][j][1])
                     
                     # if pixel is nonwhite but board says its blank, we have an update
                     if not pix_equal(pix, (255, 255, 255)) and board[i][j] == 0:
                         board_move(board, j, pos.turn)
                         pos = pos.move(j)
                         found_move = True
     return board, pos
 
grid = None
while grid is None:            
    grid = pyautogui.locateOnScreen('grid.png', confidence = 0.95)
print("Found grid")
board, pos = run(grid)