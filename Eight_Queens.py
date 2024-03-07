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
board_list = []
queen_pairs_list = []


def place_queen(board, col, row):
    # row and col -1 due to 0-index

    # place the fixed queen, if not in the fixed column place in sequential row and random row
    if col == fixed_queen_pos[1]:  # Check if the current column matches the fixed queen column
        board[8 - fixed_queen_pos[1]][col] = '∆'
        # print('Fixed ∆ placed at (' + str(col + 1) + ', ' + str(fixed_queen_pos[1]) + ')')
    else:
        board[7 - row][col] = 'Q'
        # print('Queen placed at (' + str(col + 1) + ', ' + str(row + 1) + ')')


def remove_queen(board, col, row):
    # row and col -1 due to 0-index
    board[row - 1][col] = '.'


def convert_coords(row, col):
    row_index = 8 - row
    col_index = col - 1

    return row_index, col_index


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
    threat_arr = []
    for i in range(len(arr)-1):
        if board[row][i] == 'Q':
            arr[i] = board[row][i]
            threat_arr.append((row, i))
    return arr, threat_arr


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
    if threat_arr[0]:
        threat_arr.pop()
    return ll_arr, threat_arr


# def eval_threats(board):


def calculate_heuristic(board):
    # REMEMBER TO SWITCH IT BACK TO ∆ WHEN STORING AND DISPLAYING
    board[8 - fixed_queen_pos[1]][fixed_queen_pos[0] - 1] = 'Q'

    # Initialize the array with zeros
    heuristics = [[0 for _ in range(board_size)] for _ in range(board_size)]



    # loop columns
    for i in range(0, board_size):

        q_list = []

        curr_q_row = get_col(board, i).index('Q')
        side_func = get_row(board, curr_q_row)[1]

        for _ in range(len(side_func)):
            arr = side_func
            side = ((curr_q_row, i), arr[_])

            if side not in q_list and side[::-1] not in q_list and not (curr_q_row, i) == arr[_]:
                q_list.append(side)

        ul_func = get_UL(board, curr_q_row, i)[1]

        if len(ul_func) > 0:
            for _ in range(len(ul_func)):
                arr = ul_func
                ul = ((curr_q_row, i), arr[_])
                if ul not in q_list and ul[::-1] not in q_list and not (curr_q_row, i) == arr[_]:
                    q_list.append(ul)

        ur_func = get_UR(board, curr_q_row, i)[1]
        if len(ur_func) > 0:
            for _ in range(len(ur_func)):
                arr = ur_func
                ur = ((curr_q_row, i), arr[_])
                if ur not in q_list and ur[::-1] not in q_list and not (curr_q_row, i) == arr[_]:
                    q_list.append(ur)

        ll_func = get_LL(board, curr_q_row, i)[1]
        if len(ll_func) > 0:
            for _ in range(len(ll_func)):
                arr = ll_func
                ll = ((curr_q_row, i), arr[_])
                if ll not in q_list and ll[::-1] not in q_list and not (curr_q_row, i) == arr[_]:
                    q_list.append(ll)

        lr_func = get_LR(board, curr_q_row, i)[1]
        if len(lr_func) > 0:
            for _ in range(len(lr_func)):
                arr = lr_func
                lr = ((curr_q_row, i), arr[_])
                if lr not in q_list and lr[::-1] not in q_list and not (curr_q_row, i) == arr[_]:
                    q_list.append(lr)

    print(q_list)
    h = len(q_list)
    print(h)

    return heuristics


# Randomly place queens in the other columns
for col in range(board_size):  # 0..7
    row = random.randint(0, board_size - 1)  # 0..7
    place_queen(chessboard, col, row)

# Display the board
for row in chessboard:
    print('  '.join(row))

# print(threatened(chessboard, fixed_queen_pos[0], fixed_queen_pos[1]))

x, y = convert_coords(2, 3)

calculate_heuristic(chessboard)
# for _ in calculate_heuristic(chessboard):
#     print(' '.join(str(_)))

# print(get_row(chessboard, x))
# print(get_col(chessboard, y))
# print(get_UR(chessboard, x, y))
# print(get_UL(chessboard, x, y))
# print(get_LR(chessboard, x, y))
# print(get_LL(chessboard, x, y))
