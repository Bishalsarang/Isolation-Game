


directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]

def find_piece_position(grid, piece_name):
    for i in range(7):
        for j in range(7):
            if grid[i][j] == piece_name:
                return i, j

def number_of_blank_spaces(grid):
    cnt = 0
    for i in range(7):
        for j in range(7):
            if grid[i][j] == '_':
                cnt += 1
    return cnt

def is_valid(row, col):
    return row >= 0 and col >= 0 and row < 7 and col < 7