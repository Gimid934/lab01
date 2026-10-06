from typer.testing import CliRunner

from src.toolkit.__main__ import app
from src.toolkit.constants import (
    ERR_2BINARY,
    ERR_3OPERS,
    ERR_BANNED,
    ERR_BELOW0,
    ERR_BLANK,
    ERR_CONV,
    ERR_DIV_BY_0,
    ERR_INVALID,
    ERR_MISSING_OPER,
    ERR_NOT_EXIST,
    ERR_STARTNUM,
)
from src.toolkit.core_calc import daemon as calculate
from src.toolkit.core_conv import daemon as conv


def test_calc_basic():
    assert calculate('2 + 3 * 4') == 14
    assert calculate('10 / 4') == 2.5
    assert calculate('2 * -3') == -6
    assert calculate('15 - 20') == -5


def test_calc_floats():
    assert calculate('52.9 - 2.7') <= 50.2 + 0.1**3
    assert calculate('50 / -8') == -6.25
    assert calculate('1.7 * 0.2') == 0.34
    assert calculate('6.7 + -1.2') == 5.5


def test_calc_errors():
    assert calculate('1 +- 2') == ERR_BANNED + '+-'
    assert calculate('2 * / 3') == ERR_2BINARY + '* /'
    assert calculate('2 + a') == ERR_INVALID + 'a'
    assert calculate('1 / 0') == ERR_DIV_BY_0
    assert calculate('5 - --4') == ERR_3OPERS
    assert calculate('') == ERR_BLANK
    assert calculate('/5') == ERR_STARTNUM
    assert calculate('4 8') == ERR_MISSING_OPER + '4 8'


def test_conv_basic():
    assert conv(1000.0, 'mm', 'm') == 1.0
    assert conv(46.0, 'km', 'cm') == 4600000.0
    assert conv(1.5, 'kg', 'g') == 1500
    assert conv(0.0, 'c', 'f') == 32
    assert conv(-273.15, 'c', 'k') == 0


def test_conv_uppercase():
    assert conv(2.0, 'Kg', 'g') == 2000
    assert abs(conv(160.0, 'K', 'c')-(-113.15)) <= 0.1**3
    assert abs(conv(100.0, 'K', 'F')-(-279.67)) <= 0.1**3
    assert abs(conv(-279.67, 'f', 'K')-(100)) <= 0.1**3
    assert abs(conv(178.0, 'F', 'C')-(81.111)) <= 0.1**3
    assert conv(3000.0, 'mM', 'Km') == 0.003


def test_conv_errors():
    assert conv(1.0, 'K', 'п') == ERR_NOT_EXIST + 'п'
    assert conv(67.67, 'C', 'Km') == ERR_CONV.format('C', 'Km')
    assert conv(-10, 'k', 'c') == ERR_BELOW0
    assert conv(-500, 'F', 'k') == ERR_BELOW0


def test_cli_calc():
    runner = CliRunner()
    result = runner.invoke(app, args='calc "50 * 400 - 10"')
    assert result.exit_code == 0
    assert '19990' in result.output


def test_cli_conv():
    runner = CliRunner()
    result = runner.invoke(app, args="convert -7 C f")
    assert result.exit_code == 0
    assert '19.4' in result.output


def test_cli_error():
    runner = CliRunner()
    result = runner.invoke(app, args='calc "100 / 0"')
    assert result.exit_code != 0
    assert ERR_DIV_BY_0 in result.output
