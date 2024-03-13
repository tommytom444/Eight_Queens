import random

# My student ID
studentID = 2261292

# Convert student ID to string
studentID_str = str(studentID)
k = int(studentID_str[-1])
l = int(studentID_str[-2])

# Define coordinates for fixed queen
fixed_queen_pos = ((k % 8) + 1, (l % 8) + 1)

# Generate the empty board
board_size = 8
chessboard = [['.' for col in range(board_size)] for row in range(board_size)]


def place_queen(board, col, row):
    # row and col -1 due to 0-index

    # place the fixed queen, if not in the fixed column place in sequential row and random row
    if col == fixed_queen_pos[1]:  # Check if the current column matches the fixed queen column
        board[8 - fixed_queen_pos[1]][col] = '∆'
    else:
        board[7 - row][col] = 'Q'


def remove_queen(board, col, row):
    # row and col -1 due to 0-index
    board[row - 1][col] = '.'

# returns an array with the input column
def get_col(board, col):
    # col -= 1
    arr = ['.' for _ in range(board_size)]
    i = 0
    for _ in board[col]:
        arr[i] = board[i][col]
        i += 1
    return arr

# returns an array with the input row
def get_row(board, row):
    arr = ['.' for _ in range(board_size)]
    for i in range(len(arr) - 1):
        if board[row][i] == 'Q':
            arr[i] = board[row][i]
    return arr

def get_UR(board, row, col):
    ur_arr = []
    threat_arr = []
    while row >= 0 and col < len(board[row]):
        ur_arr.append(board[row][col])
        if board[row][col] == 'Q':
            threat_arr.append((row, col))

        row -= 1
        col += 1
    ur_arr.pop(0)
    if len(threat_arr) > 0:
        threat_arr.pop(0)
    return ur_arr, threat_arr

def get_UL(board, row, col):
    ul_arr = []
    threat_arr = []
    while row >= 0 and col >= 0:
        ul_arr.append(board[row][col])
        if board[row][col] == 'Q':
            threat_arr.append((row, col))
        row -= 1
        col -= 1
    ul_arr.pop(0)
    if len(threat_arr) > 0:
        threat_arr.pop(0)

    return ul_arr, threat_arr


def get_LR(board, row, col):
    lr_arr = []
    threat_arr = []
    while row < len(board) and col < len(board[row]):
        lr_arr.append(board[row][col])
        if board[row][col] == 'Q':
            threat_arr.append((row, col))
        row += 1
        col += 1
    lr_arr.pop(0)
    if len(threat_arr) > 0:
        threat_arr.pop(0)
    return lr_arr, threat_arr


def get_LL(board, row, col):
    ll_arr = []
    threat_arr = []
    while row < len(board) and col >= 0:
        ll_arr.append(board[row][col])
        if board[row][col] == 'Q':
            threat_arr.append((row, col))
        row += 1
        col -= 1
    ll_arr.pop(0)
    if len(threat_arr) > 0:
        threat_arr.pop(0)
    return ll_arr, threat_arr

def calc_heuristic(board, row, col):
    isQueen = False

    h = 0

    if board[row][col] == 'Q':
        isQueen = True

    q_list = []

    ul_func = get_UL(board, row, col)
    for i in range(board_size):
        if len(ul_func) > 0:
            for _ in range(len(ul_func)):
                arr = ul_func
                ul = ((row, col), arr[_])
                if ul not in q_list and ul[::-1] not in q_list and not (row, col) == arr[_]:
                    q_list.append(ul)
                    h += 1
    print(q_list)









# Randomly place queens in the other columns
for col in range(board_size):  # 0..7
    row = random.randint(0, board_size - 1)  # 0..7
    place_queen(chessboard, col, row)

    # Display the board
for row in chessboard:
    print('  '.join(row))

calc_heuristic(chessboard,6,2)

