import sys
from typing import Annotated

import typer
from rich.console import Console

from src.toolkit.core_calc import daemon as calc_daemon
from src.toolkit.core_conv import daemon as conv_daemon

err_console = Console(stderr=True)
app = typer.Typer(help="Консольный набор утилит\
 (подробнее [команда] --help)", add_completion=False)


def print_handler(res):
    if type(res) is not str:
        print(res)
        sys.exit(0)
    else:
        err_console.print(res)
        sys.exit(2)


@app.command(context_settings={"ignore_unknown_options": True})
def calc(expr: Annotated[str,
                         typer.Argument(help='Выражение')]) -> int | float:
    '''
    Команда, реализующая функционал калькулятора с операциями + - * /
    Бинарные операции записываются через пробел. (1 + 2)
    Операции выполняются по приоритету. (2 + 3 * 4): (3 * 4), потом (12 + 2)
    Унарные операции (знак числа) записываются слитно с числом. (-3)
    Поддерживаются числа с плавывающей запятой. (3.5)
    Вывод:
    Число, результат выражения
    Или строка с ошибкой.
    '''
    print_handler(calc_daemon(expr))


@app.command(context_settings={"ignore_unknown_options": True})
def convert(
    value: Annotated[float, typer.Argument(help='Значение')],
    unit_from: Annotated[str, typer.Argument(help='Единица измерения')],
    unit_to: Annotated[str, typer.Argument(help='Единица измерения\
 после преобразования')]) -> float:
    '''
    Команда, реализующая функционал конвертации единиц измерения:
    Длины: mm, cm, m, km;
    Массы: g, kg;
    Температуры: c, f, k.
    Ввод: значение [единица измерения] [единица измерения после преобразования]
    Поддерживаются числа с плавывающей запятой. (273.15)
    Вывод:
    Число, результат преобразования
    Или строка с ошибкой.
    '''
    print_handler(conv_daemon(value, unit_from, unit_to))


if __name__ == "__main__":
    app()
