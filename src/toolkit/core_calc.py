import re
from itertools import pairwise

from src.toolkit.constants import (
    ERR_2BINARY,
    ERR_3OPERS,
    ERR_BANNED,
    ERR_BLANK,
    ERR_DIV_BY_0,
    ERR_INVALID,
    ERR_MISSING_OPER,
    ERR_STARTNUM,
)


def daemon(inp: str) -> int | float | str:
    """
    Внутренний обработчик, выполняет:
    токенизацию, валидацию, подсчёт выражения и вывод результата
    """
    tokens = tokenize(inp)
    check = validate(tokens)
    if not check[0]:
        return check[1]
    # print(to_rpn(tokens))
    res = calculate(tokens)
    return res[1]


def tokenize(inp: str) -> list[str]:
    """
    Токенизация через пробелы
    """
    tokens = inp.strip().split(' ')
    return tokens


def check_if_operator(token: str) -> bool:
    return len(token) == 1 and token in '+-*/'


def check_if_num(token: str) -> bool:
    num = r"^[+\-]?\d+\.?\d*$"
    return re.match(num, token)


def validate(tokens: list[str]) -> tuple[bool, str]:
    """
    Валидация
    Проверка различных случаев и определение ошибок
    """
    expr = ''.join(tokens)
    if expr.replace(' ', '') == "":
        return False, ERR_BLANK
    err_symb = set(expr) - set('+-*/.0123456789')
    if err_symb:
        return False, ERR_INVALID + ' '.join(err_symb)
    if '---' in expr.replace('+', '-'):
        return False, ERR_3OPERS
    if not check_if_num(tokens[0]):
        return False, ERR_STARTNUM

    for x, y in pairwise(tokens, tokens[1:]):
        if check_if_num(x) and check_if_num(y):
            return False, ERR_MISSING_OPER + f'{x} {y}'
        if check_if_operator(x) and check_if_operator(y):
            return False, ERR_2BINARY + f'{x} {y}'
        if not check_if_num(y) and not check_if_operator(y):
            return False, ERR_BANNED + f"{y}"
    return True, ''


def to_rpn(tokens: list[str]) -> list:
    """
    Перевод в польскую нотацию
    """
    expr = ''.join(tokens)
    if '.' in expr:
        to_num: float | int = float
    else:
        to_num: float | int = int

    queue = []
    stack = ['']
    priority_table = {'': -1, '+': 0, '-': 0, '*': 1, '/': 1}
    for token in tokens:
        if check_if_num(token):
            queue.append(to_num(token))
            continue
        if check_if_operator(token):
            while priority_table[stack[-1]] >= priority_table[token]:
                queue.append(stack.pop(-1))
            stack.append(token)
    stack.pop(0)
    queue += reversed(stack).copy()
    return queue


def calculate(tokens: list[str]) -> tuple[bool, int | float | str]:
    "Подсчёт, основанный на польской нотации"
    queue = to_rpn(tokens)
    stack = []
    for token in queue:
        token_type = type(token)
        if token_type is int or token_type is float:
            stack.append(token)
            continue
        if check_if_operator(token):
            b = stack.pop(-1)
            a = stack.pop(-1)
            match token:
                case '+':
                    stack.append(a+b)
                case '-':
                    stack.append(a-b)
                case '*':
                    stack.append(a*b)
                case '/':
                    if b == 0:
                        return False, ERR_DIV_BY_0
                    stack.append(a/b)
    return True, stack[0]
