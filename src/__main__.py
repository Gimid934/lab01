import typer
import sys
from typing import Annotated
from rich.console import Console
from .core_calc import daemon as calc_daemon
from .core_conv import daemon as conv_daemon

err_console = Console(stderr=True)
app = typer.Typer()


@app.command(context_settings={"ignore_unknown_options": True})
def calc(expr: Annotated[str, typer.Argument()]) -> int | float:
    res = calc_daemon(expr)
    if res[0]:
        print(res[1])
        sys.exit(0)
    else:
        err_console.print(res[1])
        sys.exit(2)


@app.command(context_settings={"ignore_unknown_options": True})
def convert(value: Annotated[float, typer.Argument()],
            unit_from: Annotated[str, typer.Argument()],
            unit_to: Annotated[str, typer.Argument()]) -> float:
    res = conv_daemon(value, unit_from, unit_to)
    if res[0]:
        print(res[1])
        sys.exit(0)
    else:
        err_console.print(res[1])
        sys.exit(2)


if __name__ == "__main__":
    app()
