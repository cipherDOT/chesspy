from sys import exit
import pygame
pygame.init()

file = 8
rank = 8
width = 800
height = 800
rez = width // file
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")
font = pygame.font.Font("./assets/custom_fonts/Poppins/Poppins-Light.ttf", 24)
peice_image = pygame.image.load("./assets/pieces.png").convert_alpha()

def clip(surface, x, y, x_size, y_size, _rez):
    handle_surface = surface.copy()
    clipRect = pygame.Rect(x,y,x_size,y_size)
    handle_surface.set_clip(clipRect)
    image = surface.subsurface(handle_surface.get_clip())
    image = pygame.transform.scale(image, (_rez, _rez))
    return image


class Color():
    White = (255, 255, 255)
    Black = (0, 0, 0)

    # chess.com blues theme
    Light = (123,162,192)  # light blue tiles
    Dark = (76,125,165)    # dark blue tiles
    Invert = {
        White : Black,
        Black : White,
        Light : Dark,
        Dark : Light
    }

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
                    display.blit(piece, (rank * self.rez, file * self.rez))
                else:
                    blank = font.render(' ', 1, Color.Black)
                    display.blit(blank, (rank * self.rez, file * self.rez))

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
    initial_fen = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1"
    chess_board = ChessBoard((0, 0), initial_fen, width // 8)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        chess_board.draw()
        pygame.display.flip()

if __name__ == "__main__":
    main()

