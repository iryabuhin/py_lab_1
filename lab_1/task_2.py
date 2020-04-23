import numpy as np
import re
from typing import List, Tuple, Union


def gaussian_elimination(A, B):
    A = np.array(A, float)
    B = np.array(B, float)
    
    n = len(B)
    x = np.zeros(n, float)

    # основной цикл
    for k in range(n - 1):
        for i in range(k + 1, n):
            if A[i][k] == 0:
                continue
            
            factor = A[k][k] / A[i][k]
    
            for j in range(k, n):
                A[i][j] = A[k][j] - A[i][j] * factor
    
            B[i] = B[k] - B[i] * factor


    # обратная замена иксов
    x[n-1] = B[n-1] / A[n-1][n-1]
    for i in range(n - 1, -1, -1):
        sum_x = 0
        for j in range(i + 1, n):
            sum_x += A[i][j] * x[j]
        x[i] = (B[i] - sum_x) / A[i][i]
        
    return [round(element, 2) for element in x.tolist()]


def matrix_method(A: List[List[int]], B: List[int]):
    A = np.array(A)
    B = np.array(B)
    
    
    X = [round(x, 2) for x in np.linalg.inv(A).dot(B).tolist()]
    
    return X


def crammers_rule(A: List[List[int]], B: List[int]):
    A = np.array(A)
    B = np.array(B)
    
    # удовстоверяемся в том, что переданная матрица коэфф. является квадратной
    m, n = A.shape[-2:]
    
    if m != n:
        raise ValueError('Переданная матрица должна быть квадратной (n x n)!')
    elif B.size != n:
        raise ValueError('Вектор свободных коэфф. должен быть одного размера с матрицей коэффицентов!')
    
    x = []
    tmp_matrix = np.array([row for row in A])
    det_A = round(np.linalg.det(A), 1)
    
    for i in range(len(B)):
        for j in range(len(B)):
            tmp_matrix[j][i] = B[j]
            
            if i > 0:
                tmp_matrix[j][i-1] = A[j][i-1]
            
        x.append(round(np.linalg.det(tmp_matrix) / det_A, 2))
            
    return x


def parse_equation(expr: str) -> List[int]:
    regex = r'(\b[a-z]\b|[+-]?\d+)'
    expr = re.findall(regex, expr)
    
    # заменяем переменные без индекса (например 'y', 'x') на единицу, если такие имеются
    for i in range(len(expr)):
        if expr[i].islower():
            expr[i] = '1'
    
    return [float(x) for x in expr]


    

def main():
    matrix = [] 
    
    while True:
        try:
            filename = input('Имя файла (или полный путь к нему): ')
            lines = open(filename, 'r').read().splitlines()
            break
        except FileNotFoundError:
            print('Файл  "' + filename + '" не найден!')
            print('Попробуйте ещё раз!')
            continue
            
    matrix = [parse_equation(l) for l in lines if l != '']
    
    A = []
    for row in matrix:
        A.append(row[:-1])
    
    B = [row[-1] for row in matrix]
    
    print('Матрица коэфф. уравнений и вектор свободных коэфф.:')
    for i in range(len(A)):
        print('| {} |'.format('\t'.join([str(x) for x in A[i]])), end='\t')
        print('| {} |'.format(str(B[i])))
        
    print()
    print('Выберите способ решения СЛАУ:')
    print('1) Метод Крамера')
    print('2) Метод Гаусса')
    print('3) Матричный метод')
    
    user_choice = ''
    while True:
        user_choice = input('>> ')
        if user_choice.isdigit() and int(user_choice) in [1, 2, 3]:
            user_choice = int(user_choice)
            break
        else:
            print('Некорретный ввод! Попробуйте ещё раз!')

    solution = []
    if user_choice == 1:
        solution = crammers_rule(A, B)
    elif user_choice == 2:
        solution = gaussian_elimination(A, B)
    elif user_choice == 3:
        solution = matrix_method(A, B)


    with open('solution.txt', 'w') as out_file:
        out_file.write('Решение системы:\n\t')
        out_file.write('\t'.join([str(x) for x in solution]))
    
    
    print()
    print('Решение системы записано в файл solution.txt.')

if __name__ == '__main__':
    main()
