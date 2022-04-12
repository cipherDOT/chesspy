from sys import exit

file = 8
rank = 8
board = [[0 for _ in range(rank)] for _ in range(file)]

def fen_to_board(fen):
    valid = fen.count('/') == 7
    if not valid:
        print("INVALID FEN")

    else:
        i = 0
        j = 0
        pieces_in_rank = fen.split(' ')[0].split('/')
        for pieces in pieces_in_rank:
            for notation in pieces:
                if notation.isnumeric():
                    notation = int(notation)
                    if notation <= 8:
                        j += int(notation)
                    else:
                        print("[ERROR] : Empty squares more than 8")
                        exit()
                else:
                    board[i][j] = notation
                    j += 1

            i += 1
            j = 0

    print_board(board)

def print_board(board):
    box_size = 2
    seperator = None

    for i in range(file):
        seperator = '-' * (box_size * 2 + 1)
        gap = ' ' * box_size
        print('|' + '+'.join([seperator for _ in range(rank)]) + '|')
        pieces = []
        for j in range(rank):
            pieces.append(board[i][j])

        print(f'|{gap}' + f'{gap}|{gap}'.join([str(piece) if piece != 0 else ' ' for piece in pieces]) + f'{gap}|')
    print('|' + '+'.join([seperator for _ in range(rank)]) + '|')



if __name__ == "__main__":
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b - - 0 1"
    fen_to_board(fen)

