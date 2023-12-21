from itertools import product
import math


def request_board_dimensions():
    return input("Enter your board dimensions: ")


def request_start_position():
    return input("Enter the knight's starting position: ")


def confirm_puzzle_attempt():
    return input("Do you want to try the puzzle? (y/n)")


def request_next_move():
    return input("Enter your next move: ")


class Board:
    def __init__(self):
        self.no_dimensions = True
        self.no_start_position = True
        self.no_attempt_confirmed = True

        while self.no_dimensions:
            try:
                self.dimensions = self.check_user_input(request_board_dimensions())
                self.no_dimensions = False
            except ValueError:
                print('Invalid dimensions!')

        [self.columns, self.rows] = self.dimensions
        self.number_of_cells = self.rows * self.columns
        self.cell_size = int(math.log(self.number_of_cells, 10)) + 1
        self.border_length = self.columns * (self.cell_size + 1) + 3

        while self.no_start_position:
            try:
                self.position = self.check_user_input(request_start_position())
                self.no_start_position = False
            except ValueError:
                print('Invalid position!')

        while self.no_attempt_confirmed:
            try:
                self.user_attempt = self.check_puzzle_attempt(confirm_puzzle_attempt())
                self.no_attempt_confirmed = False
            except ValueError:
                print('Invalid input!')

        self.moving_directions = [tuple(num * mul for num, mul in zip(values, combo))
                                  for values in ((1, 2), (2, 1))
                                  for combo in product([1, -1], repeat=2)]

        self.solution = self.best_possible_moves(self.position, [])

        if self.solution:
            if self.user_attempt:
                self.visited_squares = [self.position]
                self.possible_moves = self.check_moving_directions(self.position, self.visited_squares)
                self.display_chessboard()

                self.attempt_puzzle()

            else:
                print("Here's the solution!")
                self.display_chessboard(show_solution=True)
        else:
            print('No solution exists!')

    def check_user_input(self, user_in):
        user_input = user_in.split()

        if len(user_input) < 2:
            raise ValueError('Less than 2 numbers found.')
        elif len(user_input) > 2:
            raise ValueError('More than 2 numbers found.')
        else:
            int_input = tuple(int(i) for i in user_input)
            if self.in_bounds_check(int_input):
                return int_input
            else:
                raise ValueError('Number is out of bounds.')

    def check_puzzle_attempt(self, user_input):
        if user_input == 'y':
            return True
        if user_input == 'n':
            return False
        else:
            raise ValueError('Input neither "y" nor "n".')

    def in_bounds_check(self, int_input):
        x, y = int_input
        if self.no_dimensions:
            return True if x > 0 and y > 0 else False
        else:
            return True if 1 <= x <= self.dimensions[0] and 1 <= y <= self.dimensions[1] else False

    def check_moving_directions(self, position, visited_squares):
        x, y = position
        possible_moves = []
        for change_x, change_y in self.moving_directions:
            move = (x + change_x, y + change_y)
            if self.in_bounds_check(move) and move not in visited_squares:
                possible_moves.append(move)
        return possible_moves

    def best_possible_moves(self, position, visited_squares):
        current_visited_squares = visited_squares + [position]

        if len(current_visited_squares) == self.number_of_cells:
            return current_visited_squares

        current_possible_moves = self.check_moving_directions(position, current_visited_squares)

        if current_possible_moves:
            if len(current_possible_moves) > 1:
                current_possible_moves.sort(
                    key=lambda move: len(self.check_moving_directions(move, current_visited_squares)))

            for new_position in current_possible_moves:
                if best_moves_check := self.best_possible_moves(new_position, current_visited_squares):
                    return best_moves_check
                else:
                    continue
        else:
            return False

    def print_horizontal_frame(self):
        print(' ' + '-' * self.border_length)

    def display_chessboard(self, show_solution=False):
        self.print_horizontal_frame()

        for y in range(self.rows, 0, -1):
            print(f'{y}| ' + ' '.join(self.draw_cell(x, y, show_solution) for x in range(1, self.columns + 1)) + ' |')

        self.print_horizontal_frame()

        print('   ' + ' '.join(' ' * (self.cell_size - 1) + str(i) for i in range(1, self.columns + 1)))

    def draw_cell(self, x, y, show_solution):
        if show_solution:
            move_number = str(self.solution.index((x, y)) + 1)
            return ' ' * (self.cell_size - len(move_number)) + move_number

        elif (x, y) == self.position:
            return ' ' * (self.cell_size - 1) + 'X'
        elif (x, y) in self.visited_squares:
            return ' ' * (self.cell_size - 1) + '*'
        elif (x, y) in self.possible_moves:
            return ' ' * (self.cell_size - 1) + str(len(self.check_moving_directions((x, y), self.visited_squares)))
        else:
            return '_' * self.cell_size

    def attempt_puzzle(self):
        while self.possible_moves:
            try:
                next_move = self.check_user_input(request_next_move())
                if next_move in self.visited_squares:
                    raise ValueError('Square has already been visited.')
                elif next_move not in self.possible_moves:
                    raise ValueError('Illegal move.')
                else:
                    self.position = next_move
                    self.visited_squares.append(self.position)
                    self.possible_moves = self.check_moving_directions(self.position, self.visited_squares)
                    self.display_chessboard()
            except ValueError:
                print('Invalid move!', end='')

        if len(self.visited_squares) == self.number_of_cells:
            print('What a great tour! Congratulations!')
        else:
            print('No more possible moves!')
            print(f'Your knight visited {len(self.visited_squares)} squares!')


if __name__ == '__main__':
    ChessBoard = Board()
