from .constants import RATIOS_LENGTH, RATIOS_MASS, LENGTH, MASS, TEMPERATURE
from .constants import ERR_BELOW0


def daemon(value: float, unit_from: str, unit_to: str) -> tuple[bool,
                                                                float | str]:
    unit_from, unit_to = unit_from.lower(), unit_to.lower()
    if unit_from in MASS and unit_to in MASS:
        res = conv_metric(unit_from, value, unit_to, RATIOS_MASS, MASS[0])
        return True, float(res)
    if unit_from in LENGTH and unit_to in LENGTH:
        res = conv_metric(unit_from, value, unit_to, RATIOS_LENGTH, LENGTH[0])
        return True, float(res)
    if unit_from in TEMPERATURE and unit_to in TEMPERATURE:
        res = conv_temperature(unit_from, value, unit_to)
        return res
    else:
        uf, ut = unit_from, unit_to
        return False, f"Перевод из {uf} в {ut} невозможен или нереализован"


def conv_metric(unit: str, value: float, to: str,
                ratios: dict, base: str) -> float:
    if unit == to:
        return value
    if unit == base:
        return value * ratios[to]
    if to == base:
        return value / ratios[unit]
    in_base = conv_metric(unit, value, base, ratios=ratios, base=base)
    return conv_metric(base, in_base, to, ratios=ratios, base=base)


def conv_temperature(unit: str,
                     value: float,
                     to: str) -> float | tuple[bool, float | str]:
    if unit == 'c':
        if value < -273.15:
            return False, ERR_BELOW0
        if to == 'k':
            return True, float(value + 273.15)
        elif to == 'f':
            return True, float((value * 9 / 5) + 32)
    if unit == 'k':
        if value < 0:
            return False, ERR_BELOW0
        if to == 'c':
            return True, float(value - 273.15)
        elif to == 'f':
            in_c = conv_temperature('k', value, 'c')
            return True, float(conv_temperature('c', in_c, 'f'))
    if unit == 'f':
        if round(value, 2) < -459.67:
            return False, ERR_BELOW0
        if to == 'c':
            return True, float((value - 32) * 5/9)
        elif to == 'k':
            in_c = conv_temperature('f', value, 'c')
            return True, float(conv_temperature('c', in_c, 'k'))
    return False, "Такой единицы имерения не существует"
