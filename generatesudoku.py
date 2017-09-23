#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import random
import sudokusolver

def main():
    parser = argparse.ArgumentParser(description='Genereate sudoku puzzle')
    parser.add_argument('-l','--level', dest='level', type=int, default=1, help='Difficulty level (1-5)')
    parser_args = parser.parse_args()

    level = parser_args.level

    if level < 1 or level > 5:
        parser.error('Select level between 1 and 5')

    puzzle = np.zeros(9*9, dtype=np.uint8).reshape(9, 9)
    solver = sudokusolver.Solver(puzzle)
    solver.start()

    random.seed()
    
    remove_attempt_threshold = 100
    remove_attempt = 0
    while True:
        remove_x = random.randint(0,8)
        remove_y = random.randint(0,8)
        remove_val = solver.get_result()[remove_y, remove_x]
        if remove_val == 0:
            continue
        solver.set_cell(remove_y, remove_x, 0)
        solver.fill_possible_table()
        n_sol = solver.count_solutions()
        if n_sol > 1:
            solver.set_cell(remove_y, remove_x, remove_val)
            remove_attempt += 1
            if remove_attempt >= remove_attempt_threshold:
                break

    sudokusolver.print_puzzle(solver.get_result())

if __name__ == '__main__':
    main()
