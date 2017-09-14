#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import numpy as np

class Solver(object):
    table = None
    possible_table = None
    verbose = False

    def __init__(self, input_problem, verbose=False):
        self.verbose = verbose
        self.load_problem(input_problem)

    def load_problem(self, input_problem):
        if isinstance(input_problem, np.ndarray) and input_problem.ndim == 2 and \
                input_problem.shape[0] == 9 and input_problem.shape[1] == 9:
            self.table = input_problem
            self.fill_possible_table()

    def get_result(self):
        return self.table

    def start(self):
        while True:
            y, x, val = self.find_cell_with_one_possibility()

            if y < 0:
                y, x, val = self.find_one_possible_in_col()

            if y < 0:
                y, x, val = self.find_one_possible_in_row()

            if y < 0:
                y, x, val = self.find_one_possible_in_square()

            if y < 0:
                # No other results
                break

            # We found something
            if self.verbose:
                print 'X,Y = %d,%d <- %d' % (x+1, y+1, val)
            self.table[y, x] = val
            self.remove_possibility(y, x, val)

        if not self.is_solved():
            #Recursive test of possible values:
            for num_possibilities in range(2, 9):
                y, x, vals = self.find_cell_with_n_possibilities(num_possibilities)

                if y >= 0:
                    for val in vals:
                        solved_table = self.recursive_test_cell_possibility(y, x, val)
                        if solved_table is not None:
                            self.table = solved_table
                            break

    def is_solved(self):
        for i in range(9):
            if self.table[i, :].sum() != 45:
                return False
            if self.table[:, i].sum() != 45:
                return False
            sq_y = i//3
            sq_x = i%3
            if self.square(sq_y*3, sq_x*3).sum() != 45:
                return False
        # All test passed
        return True

    def find_cell_with_one_possibility(self):
        res = np.where(np.sum(self.possible_table, axis=2) == 1)
        if len(res[0]) > 0:
            y = res[0][0]
            x = res[1][0]
            val_idx = np.where(self.possible_table[y, x] == 1)[0][0]
            return y, x, val_idx+1
        return -1, -1, -1

    def find_cell_with_n_possibilities(self, num_possibilities):
        res = np.where(np.sum(self.possible_table, axis=2) == num_possibilities)
        if len(res[0]) > 0:
            y = res[0][0]
            x = res[1][0]
            val_idxs = np.where(self.possible_table[y, x] == 1)[0]
            return y, x, val_idxs+1
        return -1, -1, -1

    def find_one_possible_in_col(self):
        res = np.where(np.sum(self.possible_table, axis=1) == 1)
        if len(res[0]) > 0:
            y = res[0][0]
            val_idx = res[1][0]
            x = np.where(self.possible_table[y, :, val_idx] == 1)[0][0]
            return y, x, val_idx+1
        return -1, -1, -1

    def find_one_possible_in_row(self):
        res = np.where(np.sum(self.possible_table, axis=0) == 1)
        if len(res[0]) > 0:
            x = res[0][0]
            val_idx = res[1][0]
            y = np.where(self.possible_table[:, x, val_idx] == 1)[0][0]
            return y, x, val_idx+1
        return -1, -1, -1

    def find_one_possible_in_square(self):
        res = np.where(self.possible_table.reshape(3, 3, 3, 3, 9).sum(axis = (1, 3)) == 1)
        if len(res[0]) > 0:
            sq_y = res[0][0]
            sq_x = res[1][0]
            val_idx = res[2][0]
            relative_res = np.where(self.possible_square(sq_y*3, sq_x*3)[:, :, val_idx] == 1)
            y = sq_y*3 + relative_res[0][0]
            x = sq_x*3 + relative_res[1][0]
            return y, x, val_idx+1
        return -1, -1, -1

    def recursive_test_cell_possibility(self, y, x, val):
        new_table = self.table.copy()
        new_table[y, x] = val
        new_solver = Solver(new_table)
        new_solver.start()
        if new_solver.is_solved():
            return new_solver.get_result()
        #We found nothing
        return None


    def remove_possibility(self, y, x, value):
        self.possible_table[y, x, :] = 0 # Block filled cell
        val_idx = value - 1

        self.possible_table[:, x, val_idx] = 0
        self.possible_table[y, :, val_idx] = 0
        self.possible_square(y, x)[:, :, val_idx] = 0

    def possible_square(self, y, x):
        sq_x = x//3
        sq_y = y//3
        return self.possible_table.reshape(3, 3, 3, 3, 9)[sq_y, :, sq_x, :, :]

    def fill_possible_table(self):
        # 3rd axis for vals, 0-8 index for 1-9 vals, so val=idx+1
        self.possible_table = np.zeros(9*9*9, dtype=np.uint8).reshape(9, 9, 9)   
        for x in range(9):
            for y in range(9):
                if self.table[y, x] == 0:
                    possible_vals = self.get_possible_vals(y, x)
                    for val in possible_vals:
                        self.possible_table[y, x, val-1] = 1


    def get_possible_vals(self, y, x):
        crossed_cells = []
        crossed_cells.extend(self.row(y))
        crossed_cells.extend(self.col(x))
        crossed_cells.extend(self.square(y, x).flatten())

        forbidden_vals = set(crossed_cells)

        if 0 in forbidden_vals:
            forbidden_vals.remove(0)

        possible_vals = [val for val in range(1, 10) if val not in forbidden_vals]
        return possible_vals

    def row(self, y):
        return self.table[y, :]

    def col(self, x):
        return self.table[:, x]

    def square(self, y, x):
        sq_x = x//3
        sq_y = y//3
        return self.table.reshape(3, 3, 3, 3)[sq_y, :, sq_x, :]


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

    return np.array(array, dtype=np.uint8)

def print_puzzle(table):
    for y in range(9):
        if y == 3 or y == 6:
            print '------+-------+-------'
        for x in range(9):
            if x == 3 or x == 6:
                print '|',
            val = table[y, x]
            if val == 0:
                print '.',
            else:
                print val,
        print ''


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

    solver = Solver(input_problem)

    # solver.test_solver()
    solver.start()
    print_puzzle(solver.get_result())

if __name__ == '__main__':
    main()
