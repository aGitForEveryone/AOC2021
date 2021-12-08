from aocd import data, submit
import numpy as np


class BingoBoard:
    num_rows = 5
    num_cols = 5

    def __init__(self, board_string):
        rows = board_string.split('\n')
        self.board = np.array([[int(num.strip()) for num in row.split()] for row in rows])
        self.number_appeared = np.zeros_like(self.board)

    def update(self, number):
        self.add_number(number)
        if self.is_bingo():
            return number * self.sum_unchecked_numbers()
        else:
            return None

    def add_number(self, number):
        self.number_appeared[self.board == number] = 1

    def show_board(self):
        print(self.board)

    def is_bingo(self):
        return any(np.sum(self.number_appeared, 1) == self.num_rows) or any(np.sum(self.number_appeared, 0) == self.num_cols)

    def sum_unchecked_numbers(self):
        return np.sum(self.board[self.number_appeared == 0])


data = data.split('\n\n')
numbers = [int(x) for x in data[0].split(',')]
boards = [BingoBoard(board) for board in data[1:]]
first_bingo_found = False
boards_with_bingo = []
boards_to_skip = []

for input_idx, num in enumerate(numbers):
    # print(f'Bingo number: {num}')
    for board_idx, board in enumerate(boards):
        if board_idx in boards_to_skip:
            continue
        answer = board.update(num)
        if not first_bingo_found and answer is not None:
            print(f'First board to bingo is board {board_idx + 1}.  Bingo achieved at input {input_idx + 1}: {num}.')
            board.show_board()
            submit(answer, part='a')
            first_bingo_found = True
        if answer is not None:
            boards_with_bingo.append((board_idx, answer))
            boards_to_skip.append(board_idx)

print(f'Last board to bingo is board {boards_with_bingo[-1][0] + 1}.')
boards[boards_with_bingo[-1][0]].show_board()
submit(boards_with_bingo[-1][1], part='b')