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
    else:
        board[7 - row][col] = 'Q'


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
    for i in range(len(arr) - 1):
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
def solution(board):
    solutions = 0

    return hill_climb(board)


# def random_restart(board, col):


# PARSE IN I FROM HILL CLIMB, make code easier to read and understand so you can debug better


def calc_heuristic_array(board):
    heuristics = [[0 for _ in range(board_size)] for _ in range(board_size)]

    for i in range(0, board_size):
        # reset variables for each column
        print("column: " + str(i))
        col = i
        free_positions = [0, 1, 2, 3, 4, 5, 6, 7]
        og_queen_row = get_col(board, i).index('Q')
        col_arr = get_col(board, i)
        heuristics[free_positions[og_queen_row]][col] = calculate_heuristic(board)

        # remove the index where queen originally lies
        if col_arr[og_queen_row] == 'Q':
            free_positions.pop(og_queen_row)
        print(free_positions)
        board[og_queen_row][col] = '.'

        # loop through available positions and store their heuristic
        for index in range(0, len(free_positions)):
            row = free_positions[index]
            print("current free pos: " + str(free_positions[index]))

            if row != og_queen_row:
                board[row][col] = 'Q'
                h = calculate_heuristic(board)
                heuristics[row][col] = h
                print("heuristic: " + str(calculate_heuristic(board)))
                board[row][col] = '.'

        board[og_queen_row][col] = 'Q'
        print("NEW BOARD")
        for row in board:
            print('  '.join(row))

    return heuristics


def find_element_2d(array_2d, target):
    return [(row_idx, col_idx) for row_idx, row in enumerate(array_2d)
            for col_idx, val in enumerate(row) if val == target]


def get_lowest_value_2d(array_2d):
    flat_list = [val for row in array_2d for val in row]
    return min(flat_list)


def hill_climb(board):

    heuristics = calc_heuristic_array(board)

    min_h = get_lowest_value_2d(heuristics)

    lowest_h_poss = find_element_2d(heuristics, min_h)

    print(lowest_h_poss)
    for x in heuristics:
        print('  '.join('{:2}'.format(num) for num in x))

    if min_h == 0:
        return board

    for i in range(len(lowest_h_poss)):
        coords = lowest_h_poss[i]
        board[get_col(board, coords[1]).index('Q')][coords[1]] = '.'
        board[coords[0]][coords[1]] = 'Q'
        hill_climb(board)


def calculate_heuristic(board):
    # REMEMBER TO SWITCH IT BACK TO ∆ WHEN STORING AND DISPLAYING
    board[8 - fixed_queen_pos[1]][fixed_queen_pos[0] - 1] = 'Q'

    q_list = []

    # loop columns
    for i in range(0, board_size):

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
    h = len(q_list)

    return h


################# MAIN #####################


# Randomly place queens in the other columns
for col in range(board_size):  # 0..7
    row = random.randint(0, board_size - 1)  # 0..7
    place_queen(chessboard, col, row)

# Display the board
for row in chessboard:
    print('  '.join(row))

x, y = convert_coords(2, 3)

print(hill_climb(chessboard))
print("#########################")
