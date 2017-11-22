'''
##############################
#####Skyscrapers 6x6##########
#####By PH 11.2017############
##############################
'''
import fnmatch
import itertools
import time

SIZE = 6
#Sample clues
current_pos = 0

#init board with zeros, but you can overwrite with custom
board = [[0 for _ in range(SIZE)] for __ in range(SIZE)]

def convert_list_into_string(input_list):
    """ conver list of elements into string
    function also calculate number of visble ss from each side
    >>> convert_list_into_string([1,2,3,4,5,6])
    '61234561'
    >>> convert_list_into_string([3,2,1,4,6,5])
    '33214652'
    """
    visible_from_left = 0
    visible_from_right = 0

    current_max = 0
    for elem in input_list:
        if elem > current_max:
            current_max = elem
            visible_from_left += 1
            if elem == SIZE:
                break

    current_max = 0
    for elem in reversed(input_list):
        if elem > current_max:
            current_max = elem
            visible_from_right += 1
            if elem == SIZE:
                break

    return str(visible_from_left)+"".join([str(elm) for elm in input_list]) \
            +str(visible_from_right)

# Make a list of all permutations
DATABASE = list(itertools.permutations(range(1, SIZE+1)))
# Make a string list out of all permutations and calculate
# number of visible_from_right and visible_from_left
DATABASE_STR = [convert_list_into_string(x) for x in DATABASE]

def make_empty_field_list(input_board):
    '''basing on given input, function will creat list
    of fileds that need to be filed in order to have solution
    >>> make_empty_field_list([[1, 3, 5, 0, 6, 4],[0, 5, 4, 0, 2, 6],[0, 3, 0, 0, 0, 5],[0, 3, 0, 0, 0, 2],[1, 5, 0, 0, 0, 2], [5, 3, 4, 0, 6, 2]])[:3]
    [[0, 3], [1, 0], [1, 3]]
    '''
    empty_filed_list = []
    for irow, row in enumerate(input_board):
        for icol, col in enumerate(row):
            if col == 0:
                empty_filed_list.append([irow, icol])
    return empty_filed_list

def is_valid(ss_clues, position=current_pos, ss_board=board):
    '''will return information if certain field don't colid with valid solution
    '''
    row = str(ss_clues[SIZE*4 - 1 - position[0]])+"".join([str(x) for x in ss_board[position[0]]]) \
        + str(ss_clues[position[0]+SIZE])
    row = row.replace("0", "?")

    col = str(ss_clues[position[1]]) + "".join([str(x[position[1]]) for x in ss_board]) \
            + str(ss_clues[3*SIZE -1 -position[1]])
    col = col.replace("0", "?")

    filtered = fnmatch.filter(DATABASE_STR, col)
    if len(filtered) == 0:
        return False

    filtered = fnmatch.filter(DATABASE_STR, row)
    if len(filtered) == 0:
        return False
    return True

def current_field_val():
    return board[fields_to_fill[current_pos][0]][fields_to_fill[current_pos][1]]

def set_current_field_val(set_value):
    board[fields_to_fill[current_pos][0]][fields_to_fill[current_pos][1]] = set_value

def is_current_field_valid(clues):
    return is_valid(position=fields_to_fill[current_pos], ss_clues=clues)

fields_to_fill = make_empty_field_list(board)
current_pos = 0

def solve_puzzle(clues):
    ''' Input for function is a list of clues
        size of this list shoud be 4*SIZE
    '''
    global current_pos
    solved = False

    while not solved:
        if current_field_val() < SIZE:
            set_current_field_val(current_field_val() + 1)
            if is_current_field_valid(clues):
                current_pos = current_pos +1
                if current_pos == len(fields_to_fill):
                    solved = True
            elif current_field_val == SIZE:
                set_current_field_val(0)
                current_pos = current_pos - 1
        else:
            set_current_field_val(0)
            current_pos = current_pos - 1
    print (board)
    return board

#Example
CLUES = [6, 4, 2, 2, 2, 1, 1, 2, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 2, 2, 3, 3, 6]

CLUES = (0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0)


start_time = time.time()
solve_puzzle(CLUES)
finish_time = time.time()
print("Puzzle solved in {} s".format(finish_time-start_time))
