

# improvements to make:
#       [x] implement turn based game
#       [x] implement check rule
#       [x] implement checkmate rule
#               [ ] if all the moves of the king is also in all the moves of the enemy color, 
#                   then it's checkmate
#       [x] implement en passant
#       [ ] implement check priority rule, i.e., legal moves
#       [ ] implement castling
#       [ ] display the move log of the game

# requirements:
#       [ ] pygame
#       [ ] sys
#       [ ] time

# miscellaneous:
#       [ ] font        - Google Poppins light font  
#       [ ] color theme - chess.com "blues" color theme
# ------------------------------------------------------------------------------------------ #


# --------------------------------- required libraries ----------------------------------- #

import pygame
pygame.init()

# ---------------------------------- global variables ------------------------------------ #

file = 8
rank = 8
width = 600
height = 400
rez = height // file
display = pygame.display.set_mode((width, height))
font = pygame.font.Font("./assets/custom_fonts/Poppins/Poppins-Light.ttf", 24)
peice_image = pygame.image.load("./assets/pieces.png").convert_alpha()
logo = pygame.image.load("./assets/logo.png").convert_alpha()
pygame.display.set_caption("Chess")
pygame.display.set_icon(logo)


# ------------------------------ Utitlity Functions -------------------------------------- #
# Code to clip an image to a sub-image
def clip(surface, x, y, x_size, y_size, _rez, save=False) -> pygame.surface:
    handle_surface = surface.copy()
    clipRect = pygame.Rect(x,y,x_size,y_size)
    handle_surface.set_clip(clipRect)
    image = surface.subsurface(handle_surface.get_clip())
    image = pygame.transform.scale(image, (_rez, _rez))

    if save:
        pygame.image.save(image, "logo.png")

    return image


# ------------------------------- Utitlity Classes --------------------------------------- #

class Mousefunc(object):
    def get_square() -> tuple:
        _y, _x = pygame.mouse.get_pos()
        _x = _x // rez
        _y = _y // rez
        return (_x, _y)


# Color class
class Color():
    White = (255, 255, 255)
    Black = (0, 0, 0)
    Cyan = (100, 200, 200)

    # chess.com "blues" theme
    Light = (123,162,192)  # light blue tiles
    Dark = (76,125,165)    # dark blue tiles

    
    Invert = {
        White : Black,
        Black : White,
        Light : Dark,
        Dark : Light
    }


# ------------------------------ Game Mechanics -------------------------------------- #

# ---------------------- Piece Object ------------------- #
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


# ---------------------- Player Object ------------------- #
class Player(object):
    def __init__(self, color):
        self.color = color
        self.square_selected = False
        self.dragging = False


# A dictionary that holds the fen notation and their respective piece image 
FEN_TO_PIECE = {
    # White Pieces
    'K' : Piece.K,      # White King
    'Q' : Piece.Q,      # White Queen
    'B' : Piece.B,      # White Bishop
    'N' : Piece.N,      # White Knight
    'R' : Piece.R,      # White Rook
    'P' : Piece.P,      # White Pawn
    # # Black Pieces
    'k' : Piece.k,      # Black King
    'q' : Piece.q,      # Black Queen
    'b' : Piece.b,      # Black Bishop
    'n' : Piece.n,      # Black Knight
    'r' : Piece.r,      # Black Rook
    'p' : Piece.p       # Black Pawn
}


# ---------------------- Chess Board Object ------------------- #
class ChessBoard(object):
    def __init__(self, _pos, _fen, _rez):
        self.pos = _pos
        self.fen = _fen
        self.rez = _rez
        self.playable = True
        self.board = [[0 for _ in range(rank)] for _ in range(file)]
        self.board = self.fen_to_board()
        self.active_square = (-1, -1)
        self.active_piece = 0
        self.turn_to_move = self.fen.split()[1] == 'w'      # True if white's turn to move, False if black's turn to move
        self.player = Player("white")                       # Holds the player data
        self.white_king = None                              # position of White King
        self.black_king = None                              # position of Black King
        self.white_check = False                            # Truthy if white under check
        self.black_check = False                            # Truthy if black under check
        self.all_white_moves = []                           # has all possible moves by white
        self.all_black_moves = []                           # has all possible moves by black
        self.check_mate = False
        self.stale_mate = False
        self.en_passant_pawn = None

    # ------------------------------------------------------------------------------------ #
    def piece_color(self, piece) -> str:
        piece = str(piece)
        if piece.isupper():
            return "white"
        elif piece.islower():
            return "black"
        else:
            pass

    # ------------------------------------------------------------------------------------ #
    def refresh(self) -> None:

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 'K':
                    self.white_king = (i, j)
                if self.board[i][j] == 'k':
                    self.black_king = (i, j)

        self.all_white_moves = self.white_moves()
        self.all_black_moves = self.black_moves()

        if self.legal_moves('K', self.white_king[0], self.white_king[1]) == []:
            if self.white_king in self.all_black_moves:
                self.check_mate = True

        if self.legal_moves('k', self.black_king[0], self.black_king[1]) == []:
            if self.black_king in self.all_white_moves:
                self.check_mate = True

        if self.check_mate and self.playable:
            print("Check Mate")
            print(self.fen)
            self.playable = False
            mate_text = font.render("Check Mate!", 1, (255, 255, 255))
            display.blit(mate_text, (420, 30))

        self.all_white_moves = self.white_moves()
        self.all_black_moves = self.black_moves()

    # ------------------------------------------------------------------------------------ #
    def white_moves(self, board = None) -> list:
        if board == None:
            board = self.board

        white_moves = []

        for i in range(len(board)):
            for j in range(len(board[0])):
                if str(board[i][j]).isupper():
                    if board[i][j] == 'K':
                        self.white_king = (i, j)
                    white_moves.extend(self.legal_moves(board[i][j], i, j))

        return white_moves

    # ------------------------------------------------------------------------------------ #

    def black_moves(self, board = None) -> list:
        if board == None:
            board = self.board

        black_moves = []

        for i in range(len(board)):
            for j in range(len(board[0])):
                if str(board[i][j]).islower():
                    if board[i][j] == 'k':
                        self.black_king = (i, j)
                    black_moves.extend(self.legal_moves(board[i][j], i, j))

        return black_moves
        
    # ------------------------------------------------------------------------------------ #
    def is_enemy(self, piece1, piece2) -> bool:
        piece1 = str(piece1)
        piece2 = str(piece2)
        if piece1.isupper() and piece2.islower():
            return True
        elif piece1.islower() and piece2.isupper():
            return True
        return False
    
    # ------------------------------------------------------------------------------------ #
    def draw(self) -> None:

        for file in range(len(self.board)):
            for rank in range(len(self.board[0])):
                color = None
                if file == self.active_square[0] and rank == self.active_square[1]:
                    color = Color.Cyan
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
            if self.is_legal_move(self.active_piece, self.active_square, move):
                pygame.draw.circle(display, Color.Cyan, [move[1] * self.rez + self.rez // 2, move[0] * self.rez + self.rez // 2], 8)
        
    
    # ------------------------------------------------------------------------------------ #
    def fen_to_board(self) -> list:
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

    def board_to_fen(self, fen) -> str:
        piece_pos = ''

        for file in range(len(self.board)):
            count = 0
            for rank in range(len(self.board[0])):
                state = self.board[file][rank]
                if state == 0:
                    count += 1
                else:
                    count = '' if count == 0 else str(count)
                    piece_pos += count
                    count = 0
                    piece_pos += state

            if count == 8:
                piece_pos += '8'
            piece_pos += '/'

        piece_pos = piece_pos[:-1]
        fen = fen.split()
        fen[0] = piece_pos
        fen[1] = 'b' if self.turn_to_move else 'w'
        fen = ' '.join(fen)


        return fen

    # ------------------------------------------------------------------------------------ #

    def legal_moves(self, piece, x, y) -> list:
        # white pawn
        moves = []

        str_piece = str(piece).lower()

        match str_piece:
            case 'p':
                moves = self.pawn_moves(piece, x, y)
            case 'k':
                moves = self.king_moves(piece, x, y)
            case 'r':
                moves = self.rook_moves(piece, x, y)
            case 'b':
                moves = self.bishop_moves(piece, x, y)
            case 'n':
                moves = self.knight_moves(piece, x, y)
            case 'q':
                moves = self.rook_moves(piece, x, y)
                moves += self.bishop_moves(piece, x, y)

        # if str(piece).lower() == 'p':
        #     moves = self.pawn_moves(piece, x, y)

        # elif str(piece).lower() == 'k':
        #     moves = self.king_moves(piece, x, y)
        # # rook
        # elif str(piece).lower() == 'r':
        #     moves = self.rook_moves(piece, x, y)

        # elif str(piece).lower() == 'b':
        #     moves = self.bishop_moves(piece, x, y)

        # elif str(piece).lower() == 'n':
        #     moves = self.knight_moves(piece, x, y)

        # elif str(piece).lower() == 'q':
        #     moves = self.rook_moves(piece, x, y)
        #     moves += self.bishop_moves(piece, x, y)

        # else:
        #     pass

        return moves

    # ------------------------------------------------------------------------------------ #

    def pawn_moves(self, piece, x, y) -> list:
        moves = []

        if piece == 'P':
            if self.board[x - 1][y] == 0:
                moves.append((x - 1, y))
            if x == 6:
                if self.board[x - 2][y] == 0:
                    moves.append((x - 2, y))

            try:
                # capturing the cross-pawn
                if self.is_enemy(self.board[x - 1][y - 1], piece):
                    moves.append((x - 1, y - 1))

                # checking for en passant oppurtunity
                if self.is_enemy(self.board[x][y - 1], piece):
                    if str(self.board[x][y - 1]).lower() == 'p':
                        if (x, y - 1) == self.en_passant_pawn:
                            moves.append((x - 1, y - 1))
                
            except IndexError:
                pass

            try:
                if self.is_enemy(self.board[x - 1][y + 1], piece):
                    moves.append((x - 1, y + 1))

                if self.is_enemy(self.board[x][y + 1], piece):
                    if str(self.board[x][y + 1]).lower() == 'p':
                        if (x, y + 1) == self.en_passant_pawn:
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

                if self.is_enemy(self.board[x][y - 1], piece):
                    if str(self.board[x][y - 1]).lower() == 'p':
                        if (x, y - 1) == self.en_passant_pawn:
                            moves.append((x + 1, y - 1))

            except IndexError:
                pass

            try:
                if self.is_enemy(self.board[x + 1][y + 1], piece):
                    moves.append((x + 1, y + 1)) 

                if self.is_enemy(self.board[x][y + 1], piece):
                    if str(self.board[x][y + 1]).lower() == 'p':
                        if (x, y + 1) == self.en_passant_pawn:
                            moves.append((x + 1, y + 1))

            except IndexError:
                pass

        return moves
    # ------------------------------------------------------------------------------------ #
    # rook moves

    def rook_moves(self, piece, x, y) -> list:
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

        # right rank
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
        
        # left rank
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

        try:
            moves.remove((x, y))
        except:
            pass

        return moves

    # ------------------------------------------------------------------------------------ #
    # bishop moves

    def bishop_moves(self, piece, x, y) -> list:
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
        try:
            moves.remove((x, y))
        except:
            pass
        return moves

    # ------------------------------------------------------------------------------------ #

    def knight_moves(self, piece, x, y) -> list:
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
    # king moves

    def king_moves(self, piece, x, y) -> list:
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
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                continue
            if piece.isupper():
                if move in self.all_black_moves:
                    continue
            elif piece.islower():
                if move in self.all_white_moves:
                    continue

            square = self.board[move[0]][move[1]]
            if square == 0:
                moves.append(move)
            elif self.is_enemy(square, piece):
                board = self.board.copy()
                board[move[0]][move[1]] = 0
                if str(piece).islower():
                    enemy_moves = self.white_moves(board)
                elif str(piece).isupper():
                    enemy_moves = self.black_moves(board)

                if move not in enemy_moves:
                    moves.append(move)
                board[move[0]][move[1]] = square

        return moves
    # ------------------------------------------------------------------------------------ #

    def is_legal_move(self, piece, piece_pos, move_pos) -> bool:

        possible_moves = self.legal_moves(piece, piece_pos[0], piece_pos[1])
        # remove the capture of the kings if present in the list of legal moves.
        for move in possible_moves:
            if move == self.white_king or move == self.black_king:
                possible_moves.remove(move)

        if move_pos in possible_moves:
            return True
            
    # ------------------------------------------------------------------------------------ #

    def capture(self, capturing_piece, capturing_piece_pos, piece_to_capture_pos) -> None:
        piece_to_capture = self.board[piece_to_capture_pos[0]][piece_to_capture_pos[1]]
        self.board[capturing_piece_pos[0]][capturing_piece_pos[1]] = 0
        self.board[piece_to_capture_pos[0]][piece_to_capture_pos[1]] = capturing_piece

    # ------------------------------------------------------------------------------------ #     

    def move_piece(self, piece, piece_pos, move_pos) -> None:        
        if self.board[move_pos[0]][move_pos[1]] == 0:

            if str(self.board[move_pos[0] + 1][move_pos[1]]) == 'p' and piece == 'P':
                self.board[move_pos[0] + 1][move_pos[1]] = 0
                self.board[move_pos[0]][move_pos[1]] = piece
            
            elif str(self.board[move_pos[0] - 1][move_pos[1]]) == 'P' and piece == 'p':
                self.board[move_pos[0] - 1][move_pos[1]] = 0
                self.board[move_pos[0]][move_pos[1]] = piece
            else:
                self.board[move_pos[0]][move_pos[1]] = piece
            
            self.board[piece_pos[0]][piece_pos[1]] = 0

        else:
            self.capture(piece, piece_pos, move_pos)

        self.fen = self.board_to_fen(self.fen)

    # ------------------------------------------------------------------------------------ #     

    def check_for_en_passant(self, target_square) -> None:
        if str(self.active_piece).lower() == 'p':
            if abs(self.active_square[0] - target_square[0]) == 2:
                self.en_passant_pawn = target_square
                en_passant_fen = self.fen
                en_passant_fen = en_passant_fen.split()
                en_passant_fen[3] = ''.join(str(i) for i in target_square[::-1])
                self.fen = ' '.join(en_passant_fen)
            else:
                _fen = self.fen
                _fen = _fen.split()
                _fen[3] = '-'
                self.fen = ' '.join(_fen) 
                self.en_passant_pawn = (-1, -1) 

    # ------------------------------------------------------------------------------------ #  
    def check_for_checks(self, target_square) -> None:
        for move in self.legal_moves(self.active_piece, target_square[0], target_square[1]):
            if self.active_piece.isupper():
                if move == self.black_king:
                    self.black_check = True

            elif self.active_piece.islower():
                if move == self.white_king:
                    self.white_check = True

    # ------------------------------------------------------------------------------------ #  

    def handle_click_event(self, mouse_button) -> None:
        # seeing if the game is still playable and not in 
        # check mate or stale mate state
        if self.playable:

            # Left CLick
            if mouse_button == 1:
                selected_square = Mousefunc.get_square()
                selected_piece = self.board[selected_square[0]][selected_square[1]]
                
                # if a square was already selected by the player
                if self.player.square_selected:
                    if self.is_legal_move(self.active_piece, self.active_square, selected_square):
                        self.move_piece(self.active_piece, self.active_square, selected_square)
                        self.check_for_en_passant(selected_square)
                        self.turn_to_move = not self.turn_to_move
                        self.refresh()
                        self.check_for_checks(selected_square)

                    self.player.square_selected = False
                    self.active_square = (-1, -1)
                    self.active_piece = 0

                # if no square was selected already
                else:
                    if (str(selected_piece).isupper() and self.turn_to_move) or (str(selected_piece).islower() and not self.turn_to_move):
                        self.player.square_selected = True
                        self.active_square = selected_square
                        self.active_piece = self.board[selected_square[0]][selected_square[1]]

            # Right Click
            elif mouse_button == 3:
                self.active_square = (-1, -1)
                self.active_piece = 0

        # If the game is not playable
        else:
            print("[GAME] : Game over by check mate")


# ------------------------------------- The Main Game Loop----------------------------------------------- #
def main():
    run = True
    initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"   # inital state of a chess board
    chess_board = ChessBoard((0, 0), initial_fen, rez)
    chess_board.refresh()

    while run:
        chess_board.refresh()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                chess_board.handle_click_event(event.button)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print(chess_board.legal_moves('K', chess_board.white_king[0], chess_board.white_king[1]))
                if event.key == pygame.K_b:
                    print(chess_board.legal_moves('k', chess_board.black_king[0], chess_board.black_king[1]))

        chess_board.draw()
        pygame.display.flip()


# -------------------------------- Game Initiation ----------------------------------- #

if __name__ == "__main__":
    main()

# ------------------------------------------------------------------------------------ #
