# SUDOKU, player has the play himself
# FINISHED !!!

import numpy as np
import pandas as pd
import random as rd

# to create this Dataframe of sudoku, 9*9
# nulls = np.full((9, 9), 'x')
# board = pd.DataFrame(nulls, index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'], columns=list(range(1, 10)), )

# index_col[0] will not include Unnamed column
board = pd.read_csv('sudoku_board.csv', index_col=[0])

# the list of all row names
rows = list(board.index)
# the list of all column names
columns = list(board.columns)

additional_stuff = \
    ('''
list_positions = []
for letter in rows:
    for number in columns:
        list_positions.append(list(letter + str(number)))
''')

# an array which is 9*9, and we will be checking if the number is in the right row and column
array_rows_columns = np.full((9, 9), 'x')
# an array which is 9 times of 3*3 arrays, we'll be checking blocks 3*3, in sudoku, there must be one unique value in the block
array_blocks = np.full((9, 3, 3), 'x')

# this will add a position which corresponds to array_blocks array
# A1, A2, A3, B1, B2, B3, C1, C2, C3 is position 0
# then A4 A5 A6 B4 B5 B6 C4 C5 C6 is position 1 etc, it just goes for the number (position) of each block in array_blocks array
array_blocks_position = {}
for letter in rows:

    # for A1, A2, A3, B1, B2, B3, C1, C2, C3 is position 0
    # for A4 A5 A6 B4 B5 B6 C4 C5 C6 is position 1
    # for A7 A8 A9 B7 B8 B9 C7 C8 C9 is position 2
    if rows.index(letter) + 1 >= 1 and rows.index(letter) + 1 <= 3:
        position = 0
        for num in columns:
            array_blocks_position[letter + num] = position

            if int(num) % 3 == 0:
                position += 1

                if position > 2:
                    position = 0

    # for D1 D2 D3 E1 E2 E3 F1 F2 F3 is position 3
    # for D4 D5 D6 E4 E5 E6 F4 F5 F6 is position 4
    # for D7 D8 D9 E7 E8 E9 F7 F8 F9 is positon 5
    elif rows.index(letter) + 1 >= 4 and rows.index(letter) + 1 <= 6:
        position = 3

        for num in columns:
            array_blocks_position[letter + num] = position

            if int(num) % 3 == 0:
                position += 1

                if position > 5:
                    position = 3

    # for G1 G2 G3 H1 H2 H3 I1 H2 H3 is position 6
    # for G4 G5 G6 H4 H5 H6 I4 I5 I6 is position 7
    # for G7 G8 G9 H7 H8 H9 I7 I8 I9 is position 8
    elif rows.index(letter) + 1 >= 7  and rows.index(letter) + 1 <= 9:
        position = 6

        for num in columns:
            array_blocks_position[letter + num] = position

            if int(num) % 3 == 0:
                position += 1

                if position > 8:
                    position = 6


# columns position for only array_blocks array it is 0-2
# 3*3 block is max 2 position and min 0
# '1', '4', '7' = 0; '2', '5', '8' = 1; '3', '6', '9' = 2
column_dict = {}
# start from -1 'cause right from the start of for loop there will be +1 and we want position 0 as min
setter_name = -1
for column_name in columns:
    setter_name += 1

    column_dict[column_name] = setter_name
    # if it gets more than 2, set it again to 0
    if setter_name >= 2:
        setter_name = -1


# rows position for only array_blocks array it is 0-2
# 3*3 block is max 2 position and min 0
# 'A', 'D', 'G' = 0; 'B', 'E', 'H' = 1; 'C', 'F', 'I' = 2
row_dict = {}
# start from -1 'cause right from the start of for loop there will be +1 and we want position 0 as min
setter_name = -1
for row_name in rows:
    setter_name += 1

    row_dict[row_name] = setter_name
    # if it gets more than 2, set it again to 0
    if setter_name >= 2:
        setter_name = -1


def sudoku():
    ide = True

    # ask for the difficulty
    print('')
    version = input('What difficulty you wanna play? beginner/intermediate/expert: ').lower()

    # if beginner
    if version == 'beginner':
        # put random numbers and run this 25 times
        for _ in range(30):
            # random number between 1-9
            number = rd.randint(1, 9)

            # pick a random key in list of array_blocks_position (contains A1, A2, A3 ...)
            random_row_column = rd.choice(list(array_blocks_position.keys()))

            # random block is the value of random_row_column of array_blocks_position dict
            random_block = array_blocks_position[random_row_column]
            # random block row is the value of random_row_column[0] (A, B, C) of dict row_dict, the value is between 0-2
            random_block_row = row_dict[random_row_column[0]]
            # random block column is the value of random_row_column[1] (1, 2, 3) of dict column_dict, the value is between 0-2
            random_block_column = column_dict[random_row_column[1]]

            # if the same number appears to be in the same column, don't add it to the board just pass
            if str(number) in array_rows_columns[:, columns.index(random_row_column[1])]:
                pass

            # if the same number appears to be in the same row, don't add it to the board just pass
            elif str(number) in array_rows_columns[rows.index(random_row_column[0]), :]:
                pass

            # if the same number appears to be in the same block, don't add it to the board just pass
            elif str(number) in array_blocks[random_block, :, :]:
                pass

            # if it passes the exceptions
            else:
                # .at[row_name, int(column_name)] --> to a specific cell change
                board.at[random_row_column[0], random_row_column[1]] = str(number)

                # add that number even into the np matrix (9, 9) shape = array_row_columns
                array_rows_columns[rows.index(random_row_column[0]), columns.index(random_row_column[1])] = str(number)

                # add that number into the np matrix (9, 3, 3) shape = array_blocks
                array_blocks[random_block, random_block_row, random_block_column] = str(number)


    # if intermediate
    elif version == 'intermediate':
        # put random numbers and run this 20 times
        for _ in range(25):
            # random number between 1-9
            number = rd.randint(1, 9)

            # pick a random key in list of array_blocks_position (contains A1, A2, A3 ...)
            random_row_column = rd.choice(list(array_blocks_position.keys()))

            # random block is the value of random_row_column of array_blocks_position dict
            random_block = array_blocks_position[random_row_column]
            # random block row is the value of random_row_column[0] (A, B, C) of dict row_dict, the value is between 0-2
            random_block_row = row_dict[random_row_column[0]]
            # random block column is the value of random_row_column[1] (1, 2, 3) of dict column_dict, the value is between 0-2
            random_block_column = column_dict[random_row_column[1]]

            # if the same number appears to be in the same column, don't add it to the board just pass
            if str(number) in array_rows_columns[:, columns.index(random_row_column[1])]:
                pass

            # if the same number appears to be in the same row, don't add it to the board just pass
            elif str(number) in array_rows_columns[rows.index(random_row_column[0]), :]:
                pass

            # if the same number appears to be in the same block, don't add it to the board just pass
            elif str(number) in array_blocks[random_block, :, :]:
                pass

            # if it passes the exceptions
            else:
                # .at[row_name, int(column_name)] --> to a specific cell change
                board.at[random_row_column[0], random_row_column[1]] = str(number)

                # add that number even into the np matrix (9, 9) shape = array_row_columns
                array_rows_columns[rows.index(random_row_column[0]), columns.index(random_row_column[1])] = str(number)

                # add that number into the np matrix (9, 3, 3) shape = array_blocks
                array_blocks[random_block, random_block_row, random_block_column] = str(number)


    # if expert
    elif version == 'expert':
        # put random numbers and run this 15 times
        for _ in range(20):
            # random number between 1-9
            number = rd.randint(1, 9)

            # pick a random key in list of array_blocks_position (contains A1, A2, A3 ...)
            random_row_column = rd.choice(list(array_blocks_position.keys()))

            # random block is the value of random_row_column of array_blocks_position dict
            random_block = array_blocks_position[random_row_column]
            # random block row is the value of random_row_column[0] (A, B, C) of dict row_dict, the value is between 0-2
            random_block_row = row_dict[random_row_column[0]]
            # random block column is the value of random_row_column[1] (1, 2, 3) of dict column_dict, the value is between 0-2
            random_block_column = column_dict[random_row_column[1]]

            # if the same number appears to be in the same column, don't add it to the board just pass
            if str(number) in array_rows_columns[:, columns.index(random_row_column[1])]:
                pass

            # if the same number appears to be in the same row, don't add it to the board just pass
            elif str(number) in array_rows_columns[rows.index(random_row_column[0]), :]:
                pass

            # if the same number appears to be in the same block, don't add it to the board just pass
            elif str(number) in array_blocks[random_block, :, :]:
                pass

            # if it passes the exceptions
            else:
                # .at[row_name, int(column_name)] --> to a specific cell change
                board.at[random_row_column[0], random_row_column[1]] = str(number)

                # add that number even into the np matrix (9, 9) shape = array_row_columns
                array_rows_columns[rows.index(random_row_column[0]), columns.index(random_row_column[1])] = str(number)

                # add that number into the np matrix (9, 3, 3) shape = array_blocks
                array_blocks[random_block, random_block_row, random_block_column] = str(number)


    # if you write something other than beginner/intermediate/beginner, let him to try again
    else:
        print('')
        print('!!! You have to type a right version, beginner/intermediate/expert, try again !!!')
        sudoku()

    # actual game
    def ask():
        print('')
        print(board)

        while ide:
            print('')
            # ask for the number he wants to put in the board
            what_num = input('Which number you want to add? 1-9: ')
            try:
                _ = int(what_num)

            except ValueError:
                print('')
                print('Oops, wrong input, try again !!!')
                ask()

            # ask for the position
            what_position = input('Where do you want to put that number? (f.e. A1, B5, F3): ')

            # exception if number you want to put is between 1-9
            if int(what_num) > 9 or int(what_num) < 1:
                print('')
                print('Oops, wrong input,  try again !!!')
                ask()

            # exception if row name is correct
            if what_position[0] not in rows:
                print('')
                print('Oops, wrong input, try again !!!')
                ask()

            # exception if column name is correct
            if int(what_position[1]) < 1:
                print('')
                print('Oops, wrong input, try again !!!')
                ask()

            # if you write something like A01, A20 and something like that
            # if you write more than 1 ciferne cislo
            number_position = []
            number_position.append(what_position[1:])

            if len(number_position[0]) > 1:
                print('')
                print('Oops, wrong input, try again !!!')
                ask()

            # if that same number appears to be in the same column
            if what_num in array_rows_columns[:, int(what_position[1]) - 1]:
                print('')
                print('Cannot be duplicate number in the same column, try again !!!')
                ask()

            # if that same number appears to be in the same row
            elif what_num in array_rows_columns[rows.index(what_position[0]), :]:
                print('')
                print('Cannot be duplicate number in the same row, try again !!!')
                ask()

            # if that same number appears to be in the same block
            elif what_num in array_blocks[array_blocks_position[what_position], :, :]:
                print('')
                print('Cannot be duplicate number in the same block, try again !!!')
                ask()

            # if you write correct number
            else:
                # .at[row_name, int(column_name)] --> to a specific cell change
                board.at[what_position[0], what_position[1]] = what_num
                print('')
                print('Number added into position: ' + what_position)
                print('')
                print(board)

                # add that number even into the np matrix (9, 9) shape
                array_rows_columns[rows.index(what_position[0]), int(what_position[1]) - 1] = what_num

                # add that number into the np matrix (9, 3, 3) shape = array_blocks
                array_blocks[array_blocks_position[what_position], row_dict[what_position[0]], column_dict[what_position[1]]] = what_num

            # if the board does not contain any 'x' in it, tell him he has won
            if 'x' not in array_rows_columns[:, :]:
                print('')
                print("""YOU ARE THE TOTAL WINNER
THANK YOU FOR TRYING MY SUDOKU, BYE...""")

                exit()

    ask()


sudoku()
