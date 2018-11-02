from random import randint
from typing import *

def read_sudoku(filename: str) -> List[List[str]]: 
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values: List[List[str]]) -> None:
    """Вывод сетки Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: List[str], n: int) -> List[List[str]]:
    """
    Функция группирует значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    groups = [values[i:i + n] for i in range(0, len(values), n)]
    return groups


def get_row(values: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return values[pos[0]]


def get_col(values: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = pos[1]
    return [row[col] for row in values]


def get_block(values: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    # Остатки от деления на 3 дадут верхнюю и левую границу блока - минимумы
    top, left = 3 * (row // 3), 3 * (col // 3)
    # 2 цикла for чтобы не было списка списков
    block = [values[top + bottom][left + right] for bottom in range(3) for right in range(3)]
    return block


def find_empty_positions(grid: List[List[str]]) -> Any[Tuple[int, int], None]:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    # Объединяем все списки в один
    flat_list = [value for row in grid for value in row]
    # Если есть пустое место, вычисляем координату, иначе возращаем None
    if '.' in flat_list:
        # Находим номер свободной позиции в объединенном списке
        numero = flat_list.index('.')
        # Вычисляем координаты свободной позиции в сетке через mod и div
        row, col = numero//len(grid), numero % len(grid)
        return (row, col)
    return None


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    all_possible = set('123456789')
    row = set(get_row(grid, pos))
    col = set(get_col(grid, pos))
    block = set(get_block(grid, pos))
    return all_possible - row - col - block


def solve(grid: List[List[str]]) -> Any[List[List[str]], None]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    # Если нет пустых позиций, выводим готовое решение, иначе рекурсивно прорешиваем
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    # Иначе находим координаты пустой позиции
    row, col = pos
    # Получаем список всех возможных значений, проверяем каждое
    for possible_value in find_possible_values(grid, pos):
        # Ставим число из возможных на пустое место pos
        grid[row][col] = possible_value
        # Проверяем, есть ли потенциал у этого варианта решения
        possible_solution = solve(grid)
        if possible_solution:
            return possible_solution
        # Подходит, оставляем это число, идем к следующей пустой позиции
    # Не подошло, оставлям позицию пустой и пробуем другое число
    grid[row][col] = '.'
    return None


def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    # На вход подается список рядов
    # Проверка - сравнение сета с сетом эталона. Эталон:
    etalon = set('123456789')
    # Проверить все ряды
    for row in solution:
        if set(row) != etalon:
            return False
    # Проверить все столбцы
    for col in range(len(solution)):
        pos = (0, col)
        if set(get_col(solution, pos)) != etalon:
            return False
    # Проверить все блоки, где i, j - индексы строк и столбцов
    for i in range(0, len(solution), 3):
        for j in range(0, len(solution), 3):
            pos = (i, j)
            block = get_block(solution, pos)
            if set(block) != etalon:
                return False
    # Все тесты пройдены - вернуть True
    return True


def generate_sudoku(N: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    # На практике паззл сначала прорешивается, потом из него выкалываются точки
    # Создадим пустое поле
    grid = [['.'] * 9 for n in range(9)]

    # Прорешаем его
    grid = solve(grid) 
    # Выколем 81 - N точек
    empties = 81 - N
    # Если N <= 0, просто возвращаем grid
    if empties > 0:
        while empties:
            row, col = randint(0, 8), randint(0, 8)
            # Если не пусто - выкалываем
            if grid[row][col] != '.':
                grid[row][col] = '.'
                empties -= 1
    return grid 


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)
