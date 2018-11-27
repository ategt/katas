from functools import reduce, partial

def find_char(board, char):
    return [(x, y) for y, row in enumerate(board) for x, cell in enumerate(row) if cell == char]

def clone_boardx(board, x, y):
    board = board.copy()
    board[y] = board[y].copy()
    board[y][x] = None
    return board

def check_around(x, y, pos, dx, board, blen, rlen, limit, word):
        if board[y][x] == word[pos]:
            board = clone_boardx(board, x, y)
        
            pos = pos + 1
            
            if pos > limit:
                return True

            down_valid = blen > y + 1
            right_valid = rlen > x + 1
            up_valid = y - 1 >= 0
            left_valid = x - 1 >= 0
        
            if down_valid and dx(x, y+1, pos, dx, board):
                return True
            if up_valid and dx(x, y-1, pos, dx, board):
                return True
            if left_valid and dx(x-1, y, pos, dx, board):
                return True
            if right_valid and dx(x+1, y, pos, dx, board):
                return True
            if left_valid and down_valid and dx(x-1, y+1, pos, dx, board):
                return True
            if right_valid and down_valid and dx(x+1, y+1, pos, dx, board):
                return True
            if left_valid and up_valid and dx(x-1, y-1, pos, dx, board):
                return True
            if right_valid and up_valid and dx(x+1, y-1, pos, dx, board):
                return True
            
            return False
        else:
            return False


def check_aroundx(z, board, word, pos, blen, rlen, limit):
    dc = partial(check_around, blen=blen, rlen=rlen, limit=limit, word=word)
    
    return check_around(board=board, word=word, x=z[0], y=z[1], pos=pos, blen=blen, rlen=rlen, limit=limit, dx=dc)

def find_word(board, word):
    word = reduce(lambda acc, item: {item[0]: item[1], **acc}, enumerate(word), {})

    char = word[0]
    
    starting_coords = find_char(board, char)
    
    blen = len(board)
    rlen = len(board[0])
    limit = len(word) - 1

    cx = partial(check_aroundx, word=word, pos=0, board=board, blen=blen, rlen=rlen, limit=limit)

    return any(map(cx, starting_coords))
