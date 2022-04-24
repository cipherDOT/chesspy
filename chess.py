from ast import Index
from sys import exit
import pygame
pygame.init()

file = 8
rank = 8
width = 400
height = 400
rez = width // file
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")
font = pygame.font.Font("./assets/custom_fonts/Poppins/Poppins-Light.ttf", 24)
peice_image = pygame.image.load("./assets/pieces.png").convert_alpha()


# Code to clip an image to a sub-image
def clip(surface, x, y, x_size, y_size, _rez):
    handle_surface = surface.copy()
    clipRect = pygame.Rect(x,y,x_size,y_size)
    handle_surface.set_clip(clipRect)
    image = surface.subsurface(handle_surface.get_clip())
    image = pygame.transform.scale(image, (_rez, _rez))
    return image


class Mousefunc(object):
    def get_square():
        _x, _y = pygame.mouse.get_pos()
        _x = _x // rez
        _y = _y // rez
        # print(_x, _y)
        return (_x, _y)


# Color class
class Color():
    White = (255, 255, 255)
    Black = (0, 0, 0)
    Yellow = (100, 200, 200)

    # chess.com blues theme
    Light = (123,162,192)  # light blue tiles
    Dark = (76,125,165)    # dark blue tiles
    Invert = {
        White : Black,
        Black : White,
        Light : Dark,
        Dark : Light
    }


# Piece class.
class Piece():
    # White Pieces
    K = clip(peice_image, 0, 0, 333, 333, rez)
    Q = clip(peice_image, 333, 0, 333, 333, rez)
    B = clip(peice_image, 666, 0, 333, 333, rez) 
    N = clip(peice_image, 999, 0, 333, 333, rez)
    R = clip(peice_image, 1333, 0, 333, 333, rez)
    P = clip(peice_image, 1666, 0, 333, 333, rez)

    # Black Pieces
    k = clip(peice_image, 0, 333, 333, 333, rez)
    q = clip(peice_image, 333, 333, 333, 333, rez)
    b = clip(peice_image, 666, 333, 333, 333, rez)
    n = clip(peice_image, 999, 333, 333, 333, rez)
    r = clip(peice_image, 1333, 333, 333, 333, rez)
    p = clip(peice_image, 1666, 333, 333, 333, rez)

# A dictionary the holds the fen
# and their respective piece 
FEN_TO_PIECE = {
    # White Pieces
    'K' : Piece.K,
    'Q' : Piece.Q,
    'B' : Piece.B,
    'N' : Piece.N,
    'R' : Piece.R,
    'P' : Piece.P,
    # # Black Pieces
    'k' : Piece.k,
    'q' : Piece.q,
    'b' : Piece.b,
    'n' : Piece.n,
    'r' : Piece.r,
    'p' : Piece.p
}

# Chess Board class
class ChessBoard(object):
    def __init__(self, _pos, _fen, _rez):
        self.pos = _pos
        self.fen = _fen
        self.rez = _rez
        self.board = [[0 for _ in range(rank)] for _ in range(file)]
        self.board = self.fen_to_board()
        self.active_square = (-1, -1)
        self.active_piece = 0


    # ------------------------------------------------------------------------------------ #
    # Draw the chess board
    def draw(self):

        for file in range(len(self.board)):
            for rank in range(len(self.board[0])):
                color = None
                if file == self.active_square[0] and rank == self.active_square[1]:
                    color = Color.Yellow
                elif (file + rank) % 2 == 0:
                    color = Color.Light
                else:
                    color = Color.Dark

                pygame.draw.rect(display, color, (
                    rank * self.rez,
                    file * self.rez, 
                    # rank * self.rez + self.rez, 
                    # file * self.rez + self.rez
                    self.rez,
                    self.rez
                ))
            
                state =  str(self.board[file][rank])
                if state.isalpha():
                    piece = FEN_TO_PIECE[state]
                    display.blit(piece, (rank * self.rez, file * self.rez))
                # else:
                #     blank = font.render(' ', 1, Color.Black)
                #     display.blit(blank, (rank * self.rez, file * self.rez))

    # ------------------------------------------------------------------------------------ #
    # Given a fen string and a 2D board, this function 
    # will place the pieces in the board accordingly.
    def fen_to_board(self):
        valid = self.fen.count('/') == 7
        if not valid:
            print("[ERROR] : Invalid FEN")
        else:
            i = 0
            j = 0
            pieces_in_rank = self.fen.split(' ')[0].split('/')
            for pieces in pieces_in_rank:
                for notation in pieces:
                    if notation.isnumeric():
                        notation = int(notation)
                        if notation <= 8:
                            j += int(notation)
                        else:
                            print("[ERROR] : Invalid FEN")
                            exit()
                    else:
                        self.board[i][j] = notation
                        j += 1

                i += 1
                j = 0

        return self.board

    # ------------------------------------------------------------------------------------ #

    def board_to_fen(self):
        _fen = ''

        for file in range(len(self.board)):
            count = 0
            for rank in range(len(self.board[0])):
                state = self.board[file][rank]
                if state == 0:
                    count += 1
                else:
                    count = '' if count == 0 else str(count)
                    _fen += count
                    count = 0
                    _fen += state

            if count == 8:
                _fen += '8'
            _fen += '/'

        _fen = _fen[:-1]

        return _fen

    # ------------------------------------------------------------------------------------ #

    def legal_moves(self, piece, x, y):
        # white pawn
        moves = []
        if piece == 'P':
            if self.board[x - 1][y] == 0:
                moves.append((x - 1, y))
            if x == 6:
                if self.board[x - 2][y] == 0:
                    moves.append((x - 2, y))

            try:
                # if self.board[x - 1][y - 1] != 0 and str(self.board[x - 1][y - 1]).islower():
                if str(self.board[x - 1][y - 1]).islower():
                    moves.append((x - 1, y - 1))
            except IndexError:
                pass

            try:
                # if self.board[x - 1][y + 1] != 0 and str(self.board[x - 1][y - 1]).islower():
                if str(self.board[x - 1][y + 1]).islower():
                    moves.append((x - 1, y + 1))
            except IndexError:
                pass

        # black pawn
        elif piece == 'p':
            if self.board[x + 1][y] == 0:
                moves.append((x + 1, y))
            if x == 1:
                if self.board[x + 2][y] == 0:
                    moves.append((x + 2, y))

            try:
                if str(self.board[x + 1][y - 1]).isupper():
                    moves.append((x + 1, y - 1))   
            except IndexError:
                pass

            try:
                if str(self.board[x + 1][y + 1]).isupper():
                    moves.append((x + 1, y + 1)) 
            except IndexError:
                pass

        # if piece is 0, do nothing
        else:
            pass
        
        return moves

    # ------------------------------------------------------------------------------------ #        
    # def capture(self, capturing_piece, piece_to_capture):
    def can_move(self, piece, piece_pos, move_pos):
        # move_square = self.board[move_pos[0]][move_pos[1]]
        # if piece == 0:
        #     return False
        # elif piece_pos == move_pos:
        #     return False
        # elif str(piece).isupper() and str(move_square).isupper():
        #     return False
        # elif str(piece).islower() and str(move_square).islower():
        #     return False
        
        # # else:
        # #     self.board[move_pos[0]][move_pos[1]] = piece
        
        # # self.fen = self.board_to_fen()
        # return True
        if move_pos in self.legal_moves(piece, piece_pos[0], piece_pos[1]):
            return True

    def move(self, piece, piece_pos, move_pos):
        print(piece)
        self.board[piece_pos[0]][piece_pos[1]] = 0
        self.board[move_pos[0]][move_pos[1]] = piece

        self.fen = self.board_to_fen()
        print(self.fen)

# Main Game Loop
def main():
    run = True
    initial_fen = "rnbqkbnr/1ppp3p/p/4ppp/4PPP/8/PPPP3P/RNBQKBNR"
    # initial_fen = "rnbqkbnr/1ppp3p/p/4p1p/5PP/8/PPPP3P/RNBQKBNR"
    chess_board = ChessBoard((0, 0), initial_fen, rez)
    main_active_square = chess_board.active_square


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    
                    y, x = Mousefunc.get_square()
                    chess_board.active_square = (x, y)
                    main_active_square = chess_board.active_square
                    state = chess_board.board[main_active_square[0]][main_active_square[1]]
                    if str(state).isupper():
                        chess_board.active_piece = state
                    # print(chess_board.active_piece, main_active_square, chess_board.legal_moves(chess_board.active_piece, main_active_square[0], main_active_square[1]))
                        piece_square = main_active_square
                    
                    # print(chess_board.active_piece)

                    if chess_board.active_piece != chess_board.board[chess_board.active_square[0]][chess_board.active_square[1]]:
                        if chess_board.can_move(chess_board.active_piece, piece_square, main_active_square):
                            chess_board.move(chess_board.active_piece, piece_square, main_active_square)
                        chess_board.active_square = (-1, -1)
                        chess_board.active_piece = 0
                elif event.button == 3:
                    chess_board.active_square = (-1, -1)


        # main_active_square = chess_board.active_square
        # active_piece = chess_board.board[main_active_square[0]][main_active_square[1]] if main_active_square[0] > -1 else 0

        chess_board.draw()
        legal_moves_of_active_piece = chess_board.legal_moves(chess_board.active_piece, main_active_square[0], main_active_square[1])
        # print(legal_moves_of_active_piece)
        for move in legal_moves_of_active_piece:
            pygame.draw.circle(display, Color.Yellow, [move[1] * rez + rez // 2, move[0] * rez + rez // 2], 8)


        pygame.display.flip()


# Calling the main game loop
if __name__ == "__main__":
    main()

