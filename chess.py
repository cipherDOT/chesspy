
# ------------------------------------------------------------------------------------------ #

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
        _y, _x = pygame.mouse.get_pos()
        _x = _x // rez
        _y = _y // rez
        return (_x, _y)


# Color class
class Color():
    White = (255, 255, 255)
    Black = (0, 0, 0)
    Yellow = (100, 200, 200)

    # chess.com "blues" theme
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


class Player(object):
    def __init__(self, color):
        self.color = color
        self.square_selected = False
        self.dragging = False


# A dictionary the holds the fen and their respective piece 
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
        self.turn_to_move = True
        self.player = Player("white")
        self.white_king = None
        self.black_king = None

    def piece_color(self, piece):
        piece = str(piece)
        if piece.isupper():
            return "white"
        elif piece.islower():
            return "black"
        else:
            pass

        
    def refresh_king_positions(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 'K':
                    self.white_king = (i, j)
                elif self.board[i][j] == 'k':
                    self.black_king = (i, j)

    def is_enemy(self, piece1, piece2):
        piece1 = str(piece1)
        piece2 = str(piece2)
        if piece1.isupper() and piece2.islower():
            return True
        elif piece1.islower() and piece2.isupper():
            return True
        return False
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
                    self.rez,
                    self.rez
                ))
            
                state =  str(self.board[file][rank])
                if state.isalpha():
                    piece = FEN_TO_PIECE[state]
                    display.blit(piece, (rank * self.rez, file * self.rez))

        for move in self.legal_moves(self.active_piece, self.active_square[0], self.active_square[1]):
            pygame.draw.circle(display, Color.Yellow, [move[1] * self.rez + self.rez // 2, move[0] * self.rez + self.rez // 2], 8)

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
                if self.is_enemy(self.board[x - 1][y - 1], piece):
                    moves.append((x - 1, y - 1))
            except IndexError:
                pass

            try:
                if self.is_enemy(self.board[x - 1][y + 1], piece):
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
                if self.is_enemy(self.board[x + 1][y - 1], piece):
                    moves.append((x + 1, y - 1))   
            except IndexError:
                pass

            try:
                if self.is_enemy(self.board[x + 1][y + 1], piece):
                    moves.append((x + 1, y + 1)) 
            except IndexError:
                pass

        elif str(piece).lower() == 'k':
            moves = self.king_moves(piece, x, y)
        # rook
        elif str(piece).lower() == 'r':
            moves = self.rook_moves(piece, x, y)

        elif str(piece).lower() == 'b':
            moves = self.bishop_moves(piece, x, y)

        elif str(piece).lower() == 'n':
            moves = self.knight_moves(piece, x, y)

        elif str(piece).lower() == 'q':
            moves = self.rook_moves(piece, x, y)
            moves += self.bishop_moves(piece, x, y)


        # if piece is empty i.e., 0, do nothing
        else:
            pass
        
        return moves

    # ------------------------------------------------------------------------------------ #
    # rook moves

    def rook_moves(self, piece, x, y):
        moves = []

        # upper file
        temp_x = x - 1
        while temp_x > -1:
            square = self.board[temp_x][y]
            if  square == 0:
                moves.append((temp_x, y))
                temp_x -= 1
            elif self.is_enemy(square, piece):
                moves.append((temp_x, y))
                break
            else:
                break
        
        # lower file
        temp_x = x + 1
        while temp_x < 8:
            square = self.board[temp_x][y]
            if square == 0:
                moves.append((temp_x, y))
                temp_x += 1
            elif self.is_enemy(square, piece):
                moves.append((temp_x, y))
                break
            else:
                break
        
        temp_y = y - 1

        # upper rank
        while temp_y > -1:
            square = self.board[x][temp_y]
            if square == 0:
                moves.append((x, temp_y))
                temp_y -= 1
            elif self.is_enemy(square, piece):
                moves.append((x, temp_y))
                break
            else:        
                break
        
        # lower rank
        temp_y = y + 1
        while temp_y < 8:
            square = self.board[x][temp_y]
            if square == 0:
                moves.append((x, temp_y))
                temp_y += 1
            elif self.is_enemy(square, piece):
                moves.append((x, temp_y))
                break
            else:
                break

        return moves

    # ------------------------------------------------------------------------------------ #
    # bishop moves

    def bishop_moves(self, piece, x, y):
        moves = []

        # upper left diagonal
        temp_x = x - 1
        temp_y = y - 1
        while temp_x > -1 and temp_y > -1:
            square = self.board[temp_x][temp_y]
            if square == 0:
                moves.append((temp_x, temp_y))
                temp_x -= 1
                temp_y -= 1
            elif self.is_enemy(square, piece):
                moves.append((temp_x, temp_y))
                break
            else:
                break
        
        # lower left diagonal
        temp_x = x + 1
        temp_y = y - 1

        while temp_x < 8 and temp_y > -1:
            square = self.board[temp_x][temp_y]
            if square == 0:
                moves.append((temp_x, temp_y))
                temp_x += 1
                temp_y -= 1
            elif self.is_enemy(square, piece):
                moves.append((temp_x, temp_y))
                break
            else:
                break
        
        # upper right diagonal
        temp_x = x - 1
        temp_y = y + 1

        while temp_x > -1 and temp_y < 8:
            square = self.board[temp_x][temp_y]
            if square == 0:
                moves.append((temp_x, temp_y))
                temp_x -= 1
                temp_y += 1
            elif self.is_enemy(square, piece):
                moves.append((temp_x, temp_y))
                break
            else:        
                break
        
        # lower right diagonal
        temp_x = x + 1
        temp_y = y + 1

        while temp_x < 8 and temp_y < 8:
            square = self.board[temp_x][temp_y]
            if square == 0:
                moves.append((temp_x, temp_y))
                temp_x += 1
                temp_y += 1
            elif self.is_enemy(square, piece):
                moves.append((temp_x, temp_y))
                break
            else:
                break

        return moves

    # ------------------------------------------------------------------------------------ #

    def knight_moves(self, piece, x, y):
        possible_moves = [
            (x - 1, y - 2),
            (x - 2, y - 1),
            (x - 2, y + 1),
            (x - 1, y + 2),
            (x + 1, y - 2),
            (x + 2, y - 1),
            (x + 2, y + 1),
            (x + 1, y + 2)
        ]
        moves = []

        for move in possible_moves:
            try:
                square = self.board[move[0]][move[1]]
                if square == 0:
                    moves.append(move)
                elif self.is_enemy(square, piece):
                    moves.append(move)
            except IndexError:
                pass

        return moves

    # ------------------------------------------------------------------------------------ #

    def king_moves(self, piece, x, y):
        possible_moves = [
            (x - 1, y - 1),
            (x    , y - 1),
            (x + 1, y - 1),
            (x - 1,     y),
            (x + 1,     y),
            (x - 1, y + 1),
            (x    , y + 1),
            (x + 1, y + 1)
        ]

        moves = []

        for move in possible_moves:
            try:
                square = self.board[move[0]][move[1]]
                if square == 0:
                    moves.append(move)
                elif self.is_enemy(square, piece):
                    moves.append(move)
            except IndexError:
                pass

        return moves
    # ------------------------------------------------------------------------------------ #

    def is_legal_move(self, piece, piece_pos, move_pos):

        possible_moves = self.legal_moves(piece, piece_pos[0], piece_pos[1])
        # remove the capture of the kings if present in the list of legal moves.
        for move in possible_moves:
            if move == self.white_king or move == self.black_king:
                possible_moves.remove(move)

        if move_pos in possible_moves:
            return True

    # ------------------------------------------------------------------------------------ #

    def capture(self, capturing_piece, capturing_piece_pos, piece_to_capture_pos):
        piece_to_capture = self.board[piece_to_capture_pos[0]][piece_to_capture_pos[1]]
        self.board[capturing_piece_pos[0]][capturing_piece_pos[1]] = 0
        self.board[piece_to_capture_pos[0]][piece_to_capture_pos[1]] = capturing_piece

    # ------------------------------------------------------------------------------------ #     

    def move(self, piece, piece_pos, move_pos):        
        if self.board[move_pos[0]][move_pos[1]] == 0:
            self.board[piece_pos[0]][piece_pos[1]] = 0
            self.board[move_pos[0]][move_pos[1]] = piece
        else:
            self.capture(piece, piece_pos, move_pos)

        self.fen = self.board_to_fen()

    # ------------------------------------------------------------------------------------ #     

    def handle_click_event(self, mouse_button):
        if mouse_button == 1:
            selected_square = Mousefunc.get_square()

            if self.player.square_selected:
                if self.is_legal_move(self.active_piece, self.active_square, selected_square):
                    self.move(self.active_piece, self.active_square, selected_square)
                    self.turn_to_move = not self.turn_to_move
                    self.refresh_king_positions()
                    for move in self.legal_moves(self.active_piece, selected_square[0], selected_square[1]):
                        if self.active_piece.isupper():
                            if move == self.black_king:
                                print("Black Check")
                        elif self.active_piece.islower():
                            if move == self.white_king:
                                print("White Check")
                # else:
                #     print("[ILLEGAL MOVE]")
                self.player.square_selected = False
                self.active_square = (-1, -1)
                self.active_piece = 0

            else:
                self.player.square_selected = True
                self.active_square = selected_square
                self.active_piece = self.board[selected_square[0]][selected_square[1]]


        elif mouse_button == 3:
            self.active_square = (-1, -1)
            self.active_piece = 0

# Main Game Loop
def main():
    run = True
    # initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    initial_fen = "4r1k1/2BR1Q2/8/8/1P4P1/4P3/1P3P2/5RK1 b - - 0 42"
    # initial_fen = "8/8/8/4N/8/8/8/8"
    chess_board = ChessBoard((0, 0), initial_fen, rez)
    chess_board.refresh_king_positions()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                chess_board.handle_click_event(event.button)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print(chess_board.white_king)
                if event.key == pygame.K_b:
                    print(chess_board.black_king)


        chess_board.draw()
        pygame.display.flip()


# Calling the main game loop
if __name__ == "__main__":
    main()
