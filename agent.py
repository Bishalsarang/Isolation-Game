from collections import  namedtuple
from utilities import find_piece_position, directions, is_valid, number_of_blank_spaces
from math import hypot
import  random
from datetime import datetime
INF = float("inf")


grid = [['_' for _ in range(7)] for _ in range(7)]
grid[3][3] = 'W'
grid[4][3] = 'B'
Move = namedtuple('Move', "frm to")

class Agent():
    def __init__(self, is_max, board, depth=5):
        self.is_max = is_max
        self.depth = depth
        self.grid = board
        self.best_move = None

    def generate_move_list(self, is_max):
        moves = []
        # White piece
        if is_max:
            white_x, white_y = find_piece_position(self.grid, 'W')
            for offset_x, offset_y in directions:
                next_white_x, next_white_y = white_x + offset_x, white_y + offset_y
                if is_valid(next_white_x, next_white_y) and self.grid[next_white_x][next_white_y] == '_':
                    moves.append(Move((white_x, white_y), (next_white_x, next_white_y)))

        else:
            black_x, black_y = find_piece_position(self.grid, 'B')
            for offset_x, offset_y in directions:
                next_black_x, next_black_y = black_x + offset_x, black_y + offset_y
                if is_valid(next_black_x, next_black_y) and self.grid[next_black_x][next_black_y] == '_':
                    moves.append(Move((black_x, black_y), (next_black_x, next_black_y)))

        return moves

    def game_over(self, is_max):
        is_game_over = False
        winner = None
        # White ko pali
        if is_max:
            moves = self.generate_move_list(is_max)
            if moves:
                return False, None
            return True, "B"
        else:
            moves = self.generate_move_list(is_max)
            if moves:
                return False, None
            return True, "W"

    def calculate_heuristics(self):
        white_x, white_y = find_piece_position(self.grid, 'W')
        black_x, black_y = find_piece_position(self.grid, 'B')
        return hypot((white_x - black_x), (white_y - black_y))


    def evaluate(self, is_max):
        winner = self.game_over(is_max)
        if not winner[0]:
            white_x, white_y = find_piece_position(self.grid, 'W')
            my_moves = self.generate_move_list(is_max=True)

            black_x, black_y = find_piece_position(self.grid, 'B')
            opp_moves = self.generate_move_list(is_max=False)

            num_of_my_moves, number_of_opponent_moves, number_of_blank_space = len(my_moves), len(opp_moves), number_of_blank_spaces(self.grid)
            # Heuristics
            random.seed(datetime.now())

            return (num_of_my_moves - 2 * number_of_opponent_moves) + (number_of_blank_space / 2 + 2 * num_of_my_moves) / 13
            # return 1000 * self.calculate_heuristics() + random.random()
        if winner[1] == "B":
            return -INF
        if winner[1] == 'W':
            return INF

    def make_move(self, move,  is_max):
        frm, to = move
        x1, y1 = frm
        x2, y2 = to
        if is_max:
            self.grid[x1][y1] = 'X'
            self.grid[x2][y2] = 'W'
        else:
            self.grid[x1][y1] = 'X'
            self.grid[x2][y2] = 'B'

    def revert_move(self, move, is_max):
        frm, to = move
        x1, y1 = frm
        x2, y2 = to
        if is_max:
            self.grid[x1][y1] = 'W'
            self.grid[x2][y2] = '_'
        else:
            self.grid[x1][y1] = 'B'
            self.grid[x2][y2] = '_'

    def minimax(self, is_max, depth, alpha=-INF, beta=INF):
        score = self.evaluate(is_max)

        if depth == self.depth or abs(score) == INF:
            return score

        if is_max:
            value = -INF
            for move in self.generate_move_list(is_max):
                self.make_move(move, is_max)
                current_value = self.minimax(False, depth + 1, alpha, beta)
                alpha = max(alpha, value)
                if current_value == value and depth == 0:
                    self.best_move = move
                if current_value > value:

                    value = current_value
                    alpha = max(alpha, value)
                    if depth == 0:
                        self.best_move = move
                self.revert_move(move, is_max)

                if alpha >= beta:
                    break
            print("White: ", depth, self.best_move, value)
            return value
        else:
            value = INF
            for move in self.generate_move_list(is_max):
                self.make_move(move, is_max)
                current_value = self.minimax(True, depth + 1, alpha, beta)
                beta = min(beta, current_value)
                if current_value == value and depth == 0:
                    self.best_move = move
                if current_value < value:
                    value = current_value
                    beta = max(beta, value)
                    if depth == 0:
                        self.best_move = move
                self.revert_move(move, is_max)

                if alpha >= beta:
                    break
            print("Black: ", depth, self.best_move, value)
            return value

    def find_best_move(self):
        self.minimax(self.is_max, 0)
        return self.best_move


if __name__ == "__main__":
    ag = Agent(True, grid, 5)
    ag.find_best_move()
    print(ag.best_move)

