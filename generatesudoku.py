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

    random.seed()

    filled_cells = 30 - level*2

    solver.table[1,1] = 1

    while solver.get_solution_count() > 1:
        new_x = random.randint(0, 8)
        new_y = random.randint(0, 8)
        if solver.table[new_y, new_x] != 0:
            continue
        new_val = random.choice(solver.get_possible_vals(new_y, new_x))
        solver.table[new_y, new_x] = new_val
        val = random.randint(1, 9)
        # solver.set_cell(new_y, new_x, val)
        solver.fill_non_recursive()  

    # puzzle = solver.get_result() # Save current state
    print 'Puzzle:'
    sudokusolver.print_puzzle(solver.get_result())
    # solver.start()
    # print 'First try:',solver.is_solved()


    # solver = Solver(input_problem)

    # solver.test_solver()
    # solver.start()
    # print_puzzle(solver.get_result())

if __name__ == '__main__':
    main()