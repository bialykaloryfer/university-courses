
sudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0 ,8, 0, 0, 7, 9]
]

def is_valid(num, row, col, sudoku):
    for i in range(9):
        if sudoku[row][i] == num:
            return False
        if sudoku[i][col] == num:
            return False
        
    start_i = row // 3 * 3
    start_j = col // 3 * 3
    for i in range(3):
        for j in range(3):
            if sudoku[start_i + i][start_j + j] == num:
                return False
    return True

def solve_sudoku(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                for n in range(1, 10):
                    if is_valid(n, i, j, sudoku):
                        sudoku[i][j] = n
                        yield from solve_sudoku(sudoku)
                        sudoku[i][j] = 0
                return
    yield sudoku

for solution in solve_sudoku(sudoku):
    for row in solution:
        print(' '.join(map(str, row)))