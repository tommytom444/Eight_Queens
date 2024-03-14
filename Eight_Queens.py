import random

# my student ID
studentID = 2261292

# convert student ID to string
studentID_str = str(studentID)
k = int(studentID_str[-1])
l = int(studentID_str[-2])

# define coordinates for fixed queen
fixed_queen_pos = ((k % 8) + 1, (l % 8) + 1)

# generate the empty board
board_size = 8
chessboard = [['.' for col in range(board_size)] for row in range(board_size)]
board_list = []
queen_pairs_list = []


# place queen's in their respective positions
def place_queen(board, col, row):
    # place the fixed queen
    if col == fixed_queen_pos[1]:
        board[8 - fixed_queen_pos[1]][col] = '∆'
    else:
        board[7 - row][col] = 'Q'


def remove_queen(board, col, row):
    # row and col -1 due to 0-index
    board[row - 1][col] = '.'


# returns an array with the input column's data
def get_col(board, col):
    # col -= 1
    arr = ['.' for _ in range(board_size)]
    i = 0
    for _ in board[col]:
        arr[i] = board[i][col]
        i += 1
    return arr


# returns an array with the input row's data
def get_row(board, row):
    arr = ['.' for _ in range(board_size)]
    threat_arr = []
    for i in range(len(arr) - 1):
        if board[row][i] == 'Q':
            arr[i] = board[row][i]
            threat_arr.append((row, i))
    return arr, threat_arr


# returns an array for upper right diagonal
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


# returns an array for upper left diagonal
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


# returns an array for lower right diagonal
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


# returns an array for lower left diagonal
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


# generate 2D heuristic array for a given board
def calc_heuristic_array(board):
    # initialise 2D heuristic array
    heuristics = [[0 for _ in range(board_size)] for _ in range(board_size)]

    # loop through columns
    for i in range(0, board_size):
        # reset variables for each column
        col = i
        free_positions = [0, 1, 2, 3, 4, 5, 6, 7]
        og_queen_row = get_col(board, i).index('Q')
        col_arr = get_col(board, i)

        # calc heuristic for positions already habituated spaces
        heuristics[free_positions[og_queen_row]][col] = calculate_heuristic(board)

        # remove the index where queen originally lies
        if col_arr[og_queen_row] == 'Q':
            free_positions.pop(og_queen_row)
        board[og_queen_row][col] = '.'

        # loop through available positions and store their heuristic
        for index in range(0, len(free_positions)):
            row = free_positions[index]

            if row != og_queen_row:
                board[row][col] = 'Q'
                h = calculate_heuristic(board)
                heuristics[row][col] = h
                board[row][col] = '.'

        # place queen back in original position
        board[og_queen_row][col] = 'Q'

    # announce and output new board iteration
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


# hill climb / local beam approach to recursively solve a board
def hill_climb(board, depth=0, sideways=0, max_depth=300, max_sideways=6, prev_heuristic=None):
    if depth >= max_depth:
        return "max depth reached"

    # store heuristics, the lowest value and positions within it
    heuristics = calc_heuristic_array(board)
    min_h = get_lowest_value_2d(heuristics)
    lowest_h_positions = find_element_2d(heuristics, min_h)

    print("Depth:", depth)
    print("Heuristic:", min_h)
    print("Sideways:", sideways)
    print("Lowest H Poss:", lowest_h_positions)

    # if solved then re-format board and break
    if min_h == 0:
        coords = lowest_h_positions[0]
        board[get_col(board, coords[1]).index('Q')][coords[1]] = '.'
        board[8 - fixed_queen_pos[1]][fixed_queen_pos[0] - 1] = '∆'
        board[coords[0]][coords[1]] = 'Q'
        print("Solution found at depth:", depth)
        return board, heuristics

    # if heuristic hasn't changed go sideways
    if prev_heuristic is not None and min_h == prev_heuristic:
        sideways += 1

        # random restart once too many sideways movements made
        if sideways >= max_sideways:
            row = random.randint(0, board_size - 1)
            while row != fixed_queen_pos[0]:
                row = random.randint(0, board_size - 1)

            col = random.randint(0, board_size - 1)
            board[get_col(board, col).index('Q')][col] = '.'
            board[row][col] = 'Q'
            print("Random Restart at depth:", depth)
            return hill_climb(board, depth + 1, sideways=0, max_depth=max_depth)
    else:
        sideways = 0

    for i in range(len(lowest_h_positions)):
        coords = lowest_h_positions[i]
        board[get_col(board, coords[1]).index('Q')][coords[1]] = '.'
        board[coords[0]][coords[1]] = 'Q'
        result = hill_climb(board, depth + 1, sideways, max_depth, max_sideways, min_h)
        if result != "no result found within max depth":
            return result

    return "no result found within max depth"


# generate heuristic value for parsed in board
def calculate_heuristic(board):
    board[8 - fixed_queen_pos[1]][fixed_queen_pos[0] - 1] = 'Q'
    q_list = []

    # loop through each column
    for i in range(0, board_size):

        # get queen index for current column
        curr_q_row = get_col(board, i).index('Q')

        # array to store threats from either side
        side_func = get_row(board, curr_q_row)[1]

        # check side threats
        for _ in range(len(side_func)):
            arr = side_func
            side = ((curr_q_row, i), arr[_])
            if side not in q_list and side[::-1] not in q_list and not (curr_q_row, i) == arr[_]:
                q_list.append(side)

        # check diagonal threats
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
    return len(q_list)


################# MAIN #####################


# Randomly place queens in the other columns
for col in range(board_size):  # 0..7
    row = random.randint(0, board_size - 1)  # 0..7
    place_queen(chessboard, col, row)

# Display the board
for row in chessboard:
    print('  '.join(row))

# generate a solution using the hill climb algorithm
solution = hill_climb(chessboard)

# Check if solution is a string
if isinstance(solution, str):
    print(solution)
else:
    print('\n')
    print('Solved Board')
    # Display the board
    for row in solution[0]:
        print('  '.join(row))

    print('\n')
    print('Heuristic Table')
    # output 2D heuristic array
    for row in solution[1]:
        print(" ".join(str(cell).ljust(2) for cell in row))
