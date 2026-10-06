import re
from .constants import ERR_3OPERS, ERR_STARTNUM


def daemon(inp: str) -> tuple[bool, int | float | str]:
    tokens = tokenize(inp)
    check = validate(tokens)
    if not check[0]:
        return check
    # print(to_rpn(tokens))
    res = calculate(tokens)
    return res


def tokenize(inp: str) -> list[str]:
    tokens = inp.strip().split(' ')
    return tokens


def check_if_operator(token: str) -> bool:
    return len(token) == 1 and token in '+-*/'


def check_if_num(token: str) -> bool:
    num = r"^[+\-]?\d+\.?\d*$"
    if not re.match(num, token):
        return False
    return True


def validate(tokens: list[str]) -> tuple[bool, str]:
    expr = ''.join(tokens)
    if expr.replace(' ', '') == "":
        return False, "Дано пустое выражение"
    err_symb = set(expr) - set('+-*/.0123456789')
    if err_symb:
        return False, f"Недопустимый символ: {' '.join(err_symb)}"
    if '---' in expr.replace('+', '-'):
        return False, ERR_3OPERS
    if not check_if_num(tokens[0]):
        return False, ERR_STARTNUM

    for x, y in zip(tokens, tokens[1:]):
        if check_if_num(x) and check_if_num(y):
            return False, f'Пропущен бинарный оператор между: {x} {y}'
        if check_if_operator(x) and check_if_operator(y):
            return False, f'Два бинарных оператора подряд: {x} {y}'
        if not check_if_num(y) and not check_if_operator(y):
            return False, f"Нарушена форма записи операнда или оператора: {y}"
    return True, ''


def to_rpn(tokens: list[str]) -> list:
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
    for operator in reversed(stack):
        queue.append(operator)
    return queue


def calculate(tokens: list[str]) -> tuple[bool, int | float | str]:
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
                        return False, "Деление на 0"
                    stack.append(a/b)
    return True, stack[0]
