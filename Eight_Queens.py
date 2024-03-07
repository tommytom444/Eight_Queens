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
    i = 0
    for _ in range(board_size):
        arr[i] = board[row][i]
        i += 1
    return arr


def get_UR(board, row, col):
    ur_arr = []
    while row >= 0 and col < len(board[row]):
        ur_arr.append(board[row][col])
        row -= 1
        col += 1
    ur_arr[0] = '.'
    return ur_arr


def get_UL(board, row, col):
    ul_arr = []
    while row >= 0 and col >= 0:
        ul_arr.append(board[row][col])
        row -= 1
        col -= 1
    ul_arr[0] = '.'
    return ul_arr


def get_LR(board, row, col):
    lr_arr = []
    while row < len(board) and col < len(board[row]):
        lr_arr.append(board[row][col])
        row += 1
        col += 1
    lr_arr[0] = '.'
    return lr_arr


def get_LL(board, row, col):
    ll_arr = []
    while row < len(board) and col >= 0:
        ll_arr.append(board[row][col])
        row += 1
        col -= 1
    ll_arr[0] = '.'
    return ll_arr


def calculate_heuristic(board):
    # REMEMBER TO SWITCH IT BACK TO ∆ WHEN STORING AND DISPLAYING
    board[8 - fixed_queen_pos[1]][fixed_queen_pos[0] - 1] = 'Q'

    # Initialize the array with zeros
    heuristics = [[0 for _ in range(board_size)] for _ in range(board_size)]

    # loop columns
    for i in range(0, board_size):
        curr_q_row = get_col(board, i).index('Q')
        # print(i)
        # print(get_col(board, i))

        # get counts for each threat angle
        if get_row(board, curr_q_row).__contains__('Q'):
            heuristics[curr_q_row][i] += get_row(board, curr_q_row).count('Q')-1
        heuristics[curr_q_row][i] += get_UL(board, curr_q_row, i).count('Q')
        heuristics[curr_q_row][i] += get_UR(board, curr_q_row, i).count('Q')
        heuristics[curr_q_row][i] += get_LL(board, curr_q_row, i).count('Q')
        heuristics[curr_q_row][i] += get_LR(board, curr_q_row, i).count('Q')

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


for _ in calculate_heuristic(chessboard):
    print(' '.join(str(_)))

print(get_row(chessboard, x))
print(get_col(chessboard, y))
print(get_UR(chessboard, x, y))
print(get_UL(chessboard, x, y))
print(get_LR(chessboard, x, y))
print(get_LL(chessboard, x, y))