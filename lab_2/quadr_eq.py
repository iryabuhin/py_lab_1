import numpy as np
import re
from math import sqrt

class NotEnoughComputingPower(Exception):
    err_msg: str = ''
    
    def __init__(self, *args):
        self.err_msg = args[0]
        
    def __str__(self):
        if self.err_msg:
            return f'NotEnoughComputingPower: {self.err_msg}'
        else:
            return 'NotEnoughComputingPower raised!'


def discriminant_solve(a: int, b: int, c: int):
    D = (pow(b, 2) - 4*a*c)
    
    if D > 0:
        x1 = round((-b + sqrt(D)) / (2*a), 2)
        x2 = round((-b - sqrt(D)) / (2*a), 2)
        return x1, x2
    elif D < 0:
        complex_roots = np.roots([a, b, c])
        print('Дискриминант меньше нуля, ищем комплексные корни уравнения...')
        return complex_roots
    


def vieta_solve(a: int, b: int, c: int):
    x1, x2 = 0, 0
    possible_roots = list(range(-1000, 1000))
    
    for i in possible_roots:
        x1 = i
        for j in possible_roots:
            x2 = j
            if x1+x2 == -b/a and x1*x2 == c/a:
                return x1, x2
    
    raise NotEnoughComputingPower('Недостаточно вычислительной мощности для решения уравнения теоремой Виета')

def parse_equation(expr: str):
    regex = re.compile(r'(-?\d+)x\^*?2\s*?([+-]\d+)x\s*?([+-]\d+)\s*?=\s*?(\d+)')
    
    matches = regex.match(expr)
    
    a = float(matches.group(1))
    b = float(matches.group(2))
    c = float(matches.group(3))

    if matches.group(4):
        c -= float(matches.group(4))
    
    return [a, b, c]
    

def solve_equation(expr: str):
    coeffs = parse_equation(expr)
    a, b, c = coeffs
    roots = []
    
    try:
        roots = vieta_solve(a, b, c)
    except NotEnoughComputingPower:
        print('Не удалось решить используя теорему Виета, решаем через дискриминант...')
        roots = discriminant_solve(a, b, c)

    return roots

    with open('solution.txt', 'w') as output_file:
            output_file.write('Решение квадратного ур-я:\n\t')
            
            # если корни комплексные
            if isinstance(roots[0], complex):
                output_file.write('Комплексные корни:\n\t')
            
            output_file.write('\t'.join([str(x) for x in roots]))
            
            if not isinstance(roots[0], complex):
                output_file.write('\nПроверка подстановкой:\n')
                x1, x2 = roots
                output_file.write(f"a*x1^2 + b*x1 + c = {eval('a * x1**2 + b*x1 + c')}\n")
                output_file.write(f"a*x2^2 + b*x2 + c = {eval('a * x2**2 + b*x2 + c')}\n")
    
    print('\nРешение записано в файл solution.txt')
            
if __name__ == "__main__":
    main()      
