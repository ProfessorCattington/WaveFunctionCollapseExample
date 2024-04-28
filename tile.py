import pygame
from random import randint

#SIDE MAPPING
TOP = 0
LEFT = 1
RIGHT = 2
BOTTOM = 3

#SOCKET MAPPING
SOCKET_MAPPING = {
    0 : [0,0,0,0],
    1 : [1,1,1,1],
    2 : [0,1,1,0],
    3 : [1,0,0,1],
    4 : [1,1,0,1],
    5 : [1,0,1,1],
    6 : [1,1,1,0],
    7 : [0,1,1,1],
    8 : [1,1,1,1]
}

class Tile:
    def __init__(self, id):
        self.id = id
        self.image = None
        self.update(self.id)

    def update(self, id):
        self.id = id
        path = "git_stuff/pythonstuff/tiles/tile_0" + str(id) + ".png"
        self.image = pygame.image.load(path)

class BoardPiece:
    def __init__(self, x, y):
        self.position_x = x
        self.position_y = y
        self.tile = Tile(8)
        self.remaining_options = [0,1,2,3,4,5,6,7]
        self.entropy = 8

    def __lt__(self, other):
        return self.entropy < other.entropy

    def updatePieceId(self, id):
        self.tile.update(id)
    

class Board:
    def __init__(self, board_dimensions):
        self.grid = []
        self.board_dimensions = board_dimensions
        for i in range(board_dimensions[0]):
            row = []
            for j in range(board_dimensions[1]):
                new_piece = BoardPiece(i, j)
                row.append(new_piece)
            self.grid.append(row)
    
    def getPiece(x, y) -> BoardPiece:
        return self.grid[x][y]
    
    def collapse(self, x, y):

        board_piece = self.grid[x][y]

        if len(board_piece.remaining_options) > 1:
            new_id = randint(0, len(board_piece.remaining_options) -1)
        else:
            new_id = 0

        print(f"piece: {x}, {y} remaining options: {board_piece.remaining_options}")
        
        new_id = board_piece.remaining_options[new_id]

        #remove entropy and possible options
        board_piece.entropy = 0
        board_piece.remaining_options = [] 

        board_piece.updatePieceId(new_id)

        #update the neighbors
        if board_piece.position_x > 0:
            print(f"Updating neighbor to the left")
            neighbor_piece = self.grid[board_piece.position_x - 1][board_piece.position_y]
            self.updateNeighbor(LEFT, RIGHT, board_piece, neighbor_piece)
        if board_piece.position_y > 0:
            print(f"Updating neighbor above")
            neighbor_piece = self.grid[board_piece.position_x][board_piece.position_y - 1]
            self.updateNeighbor(TOP, BOTTOM, board_piece, neighbor_piece)
        if board_piece.position_x < self.board_dimensions[0]-1:
            print(f"Updating neighbor to the right")
            neighbor_piece = self.grid[board_piece.position_x + 1][board_piece.position_y]
            self.updateNeighbor(RIGHT, LEFT, board_piece, neighbor_piece)
        if board_piece.position_y < self.board_dimensions[1]-1:
            print(f"Updating neighbor below")
            neighbor_piece = self.grid[board_piece.position_x][board_piece.position_y + 1]
            self.updateNeighbor(BOTTOM, TOP, board_piece, neighbor_piece)
    
    def updateNeighbor(self, piece_side, neighbor_side, board_piece, neighbor_piece):

        if neighbor_piece.entropy == 0:
            return

        this_id = board_piece.tile.id
        this_socket_mapping = SOCKET_MAPPING[this_id]
        socket_type = this_socket_mapping[piece_side]

        new_options =[]
        print(f"board piece uses tile: {board_piece.tile.id}")
        print(f"neighbor: {neighbor_piece.position_x}, {neighbor_piece.position_y} had options: {neighbor_piece.remaining_options}")
        for option in neighbor_piece.remaining_options:
            potential_socket_mapping = SOCKET_MAPPING[option]
            if socket_type == potential_socket_mapping[neighbor_side]:
                new_options.append(option)
        print(f"neighbor: {neighbor_piece.position_x}, {neighbor_piece.position_y} updated options: {new_options}")

        if len(new_options) == 0:
            new_options.append(8)

        neighbor_piece.remaining_options = new_options
        neighbor_piece.entropy = len(new_options)
