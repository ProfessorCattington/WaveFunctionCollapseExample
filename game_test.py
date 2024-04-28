# import the pygame module, so you can use it
import pygame
import tile
from queue import PriorityQueue

BOARD_DIMENSIONS = [120,67]
TILE_SIZE = 32

# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("git_stuff/pythonstuff/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Grid")


    board = tile.Board(BOARD_DIMENSIONS)
    board_grid = board.grid

    piece_queue = makeQueue(board_grid)

    while piece_queue.qsize() > 0:
        piece = piece_queue.get()
        board.collapse(piece.position_x, piece.position_y)
        piece_queue = sortQueue(piece_queue)
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((TILE_SIZE * BOARD_DIMENSIONS[0], TILE_SIZE * BOARD_DIMENSIONS[1]))

    for i in range(len(board_grid)):
        for j in range(len(board_grid[0])):
            board_piece = board_grid[i][j]
            image = board_piece.tile.image
            screen.blit(image, (board_piece.position_x * TILE_SIZE, board_piece.position_y * TILE_SIZE))
    
    pygame.display.flip()
    
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
     

def makeQueue(board_grid):
    new_queue = PriorityQueue()

    for i in range(len(board_grid)):
        for j in range(len(board_grid[0])):
            if board_grid[i][j].entropy > 0:
                new_queue.put(board_grid[i][j])
    print(f"{new_queue.qsize()}")

    return new_queue

def sortQueue(old_queue): #super lazy and inefficient way
    new_queue = PriorityQueue()
    while old_queue.qsize() > 0:
        new_queue.put(old_queue.get())

    return new_queue


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
