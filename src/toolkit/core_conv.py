from src.toolkit.constants import (
    ERR_BELOW0,
    ERR_CONV,
    ERR_NOT_EXIST,
    LENGTH,
    MASS,
    RATIOS_LENGTH,
    RATIOS_MASS,
    TEMPERATURE,
)


def daemon(value: float, orig_from: str, orig_to: str) -> float | str:
    """
    Внутренний обработчик, выполняет:
    Определение категории единиц измерения и ошибок
    Запуск конвертации
    """
    unit_from, unit_to = orig_from.lower(), orig_to.lower()
    if unit_from in MASS and unit_to in MASS:
        res = conv_metric(unit_from, value, unit_to, RATIOS_MASS, MASS[0])
        return float(res)
    if unit_from in LENGTH and unit_to in LENGTH:
        res = conv_metric(unit_from, value, unit_to, RATIOS_LENGTH, LENGTH[0])
        return float(res)
    if unit_from in TEMPERATURE and unit_to in TEMPERATURE:
        res = conv_temperature(unit_from, value, unit_to)
        return res
    if unit_from not in MASS + LENGTH + TEMPERATURE:
        return ERR_NOT_EXIST + orig_from
    if unit_to not in MASS + LENGTH + TEMPERATURE:
        return ERR_NOT_EXIST + orig_to
    return ERR_CONV.format(orig_from, orig_to)


def conv_metric(unit: str, value: float, to: str,
                ratios: dict, base: str) -> float:
    """
    Конвертация единиц измерения в метрической системе
    """
    if unit == to:
        return value
    if unit == base:
        return value / ratios[to]
    if to == base:
        return value * ratios[unit]
    in_base = conv_metric(unit, value, base, ratios=ratios, base=base)
    return conv_metric(base, in_base, to, ratios=ratios, base=base)


def conv_temperature(unit: str,
                     value: float,
                     to: str) -> float | tuple[bool, float | str]:
    """
    Конвертация температуры, обработка температуры ниже абсолютного нуля
    """
    if unit == 'c':
        if value < -273.15:
            return ERR_BELOW0
        if to == 'k':
            return float(value + 273.15)
        elif to == 'f':
            return float((value * 9 / 5) + 32)
    if unit == 'k':
        if value < 0:
            return ERR_BELOW0
        if to == 'c':
            return float(value - 273.15)
        elif to == 'f':
            in_c = conv_temperature('k', value, 'c')
            return float(conv_temperature('c', in_c, 'f'))
    if unit == 'f':
        if round(value, 2) < -459.67:
            return ERR_BELOW0
        if to == 'c':
            return float((value - 32) * 5/9)
        elif to == 'k':
            in_c = conv_temperature('f', value, 'c')
            return float(conv_temperature('c', in_c, 'k'))
    return ERR_NOT_EXIST
