from sys import exit
from matplotlib.pyplot import pie
import pygame
pygame.init()

file = 8
rank = 8
board = [[0 for _ in range(rank)] for _ in range(file)]
width = 400
height = 400
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")
font = pygame.font.Font("./assets/custom_fonts/Poppins/Poppins-Light.ttf", 24)
peice_image = pygame.image.load("./assets/pieces.png").convert_alpha()

def clip(surface, x, y, x_size, y_size):
    handle_surface = surface.copy()
    clipRect = pygame.Rect(x,y,x_size,y_size)
    handle_surface.set_clip(clipRect)
    image = surface.subsurface(handle_surface.get_clip())
    image = pygame.transform.scale(image, (50, 50))
    # pygame.image.save(image, f"{name}.png")
    return image


class Color():
    White = (255, 255, 255)
    Black = (0, 0, 0)
    Light = (185, 123, 101)
    Dark = (100, 59, 46)
    Invert = {
        White : Black,
        Black : White,
        Light : Dark,
        Dark : Light
    }

class Piece():
    # White Pieces
    K = clip(peice_image, 0, 0, 333, 333)
    Q = clip(peice_image, 333, 0, 333, 333)
    B = clip(peice_image, 666, 0, 333, 333) 
    N = clip(peice_image, 999, 0, 333, 333)
    R = clip(peice_image, 1333, 0, 333, 333)
    P = clip(peice_image, 1666, 0, 333, 333)

    # Black Pieces
    k = clip(peice_image, 0, 333, 333, 333)
    q = clip(peice_image, 333, 333, 333, 333)
    b = clip(peice_image, 666, 333, 333, 333)
    n = clip(peice_image, 999, 333, 333, 333)
    r = clip(peice_image, 1333, 333, 333, 333)
    p = clip(peice_image, 1666, 333, 333, 333)

fen_to_peice = {
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


class ChessBoard(object):
    def __init__(self, _pos, _fen, _rez):
        self.pos = _pos
        self.fen = _fen
        self.rez = _rez
        self.board = [[0 for _ in range(rank)] for _ in range(file)]
        self.board = self.fen_to_board()


    def draw(self):
        for file in range(len(self.board)):
            for rank in range(len(self.board[0])):
                color = None
                if (file + rank) % 2 == 0:
                    color = Color.Light
                else:
                    color = Color.Dark

                pygame.draw.rect(display, color, (
                    rank * self.rez,
                    file * self.rez, 
                    rank * self.rez + self.rez, 
                    file * self.rez + self.rez
                ))

                state =  str(self.board[file][rank])
                if state.isalpha():
                    piece = fen_to_peice[state]
                    # piece = pygame.transform.scale(piece, (self.rez, self.rez))
                    display.blit(piece, (rank * self.rez, file * self.rez))
                else:
                    blank = font.render(' ', 1, Color.Black)
                    display.blit(blank, (rank * self.rez, file * self.rez))

                # pygame.display.update((
                #     rank * self.rez,
                #     file * self.rez, 
                #     rank * self.rez + self.rez, 
                #     file * self.rez + self.rez
                # ))

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

def main():
    run = True
    initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    chess_board = ChessBoard((0, 0), initial_fen, width // 8)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        chess_board.draw()
        pygame.display.flip()

if __name__ == "__main__":
    main()

