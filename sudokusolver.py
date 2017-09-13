#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import numpy as np

def parse_sudoku_file(sudoku_file):
    array = []
    with open(sudoku_file, 'r') as input_file:
        for line in input_file:
            str_row = line.split()
            row = [int(elem) for elem in str_row]
            if len(row) != 9:
                return None
            array.append(row)

    if len(array) != 9:
        return None

    return np.array(array, dtype=np.uint32)

def get_possible_nums(y, x, array):
    check = range(1, 10) #1-9
    for i in range(9):
        if array[y, i] > 0:
            check[array[y,i]-1] = 0
        if array[i, x] > 0:
            check[array[i,x]-1] = 0

    square_x = x//3
    square_y = y//3

    square = array[3*square_y:3*(square_y+1), 3*square_x:3*(square_x+1)].flatten()

    for el in square:
        if el > 0:
            check[el-1] = 0

    return [el for el in check if el > 0]



def main():
    parser = argparse.ArgumentParser(description='Solve sudoku problems')
    parser.add_argument("sudoku_input", help="Input sudoku file")
    parser_args = parser.parse_args()

    sudoku_input = parser_args.sudoku_input

    if not os.path.exists(sudoku_input):
        parser.error('Input file do not exist')
    elif not os.path.isfile(sudoku_input):
        parser.error('Input is not a file')

    input_problem = parse_sudoku_file(sudoku_input)

    if input_problem is None:
        parser.error('Wrong input format')

    print 'Start =\n',input_problem

    possible_nums = np.zeros(9*9*9,dtype=np.uint32).reshape(9, 9, 9)

    while True:
        for x in range(9):
            for y in range(9):
                possible_nums[y,x,:] = 0
                if input_problem[y,x] == 0:
                    possible_res = get_possible_nums(y, x, input_problem)
                    for el in possible_res:
                        possible_nums[y,x,el-1] = 1

        # print np.sum(posible_nums,axis=2)

        y_ind, x_ind = np.where(np.sum(possible_nums,axis=2) == 1)

        if len(y_ind) > 0:
            y = y_ind[0]
            x = x_ind[0]
            val = np.where(possible_nums[y,x] == 1)[0][0] + 1
            print 1, y,x,val
            input_problem[y,x] = val
            possible_nums[y,x,:] = 0
            continue


        y_ind, val_ind = np.where(np.sum(possible_nums,axis=1) == 1)
        if len(y_ind) > 0:
            y = y_ind[0]
            val = val_ind[0]
            x = np.where(possible_nums[y,:,val] == 1)[0][0]
            print 2, y,x,val+1
            input_problem[y,x] = val+1
            possible_nums[y,x,:] = 0
            continue

        x_ind, val_ind = np.where(np.sum(possible_nums,axis=0) == 1)
        if len(x_ind) > 0:
            x = x_ind[0]
            val = val_ind[0]
            y = np.where(possible_nums[:,x,val] == 1)[0][0]
            print 3, y,x,val+1
            input_problem[y,x] = val+1
            possible_nums[y,x,:] = 0
            continue

        break

    print 'Pos =\n',np.sum(possible_nums,axis=2)
    print 'Result =\n',input_problem


if __name__ == '__main__':
    main()
