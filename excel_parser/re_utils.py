import re

cab_pattern = re.compile("[0-9]{3}[а-яА-Я]?")


def match_cab(e_val):
    possible_cab = e_val.split()[-1]
    return cab_pattern.match(possible_cab)


def contains_cabinet(e_val: str):
    return bool(match_cab(e_val))


def get_cab(e_val):
    return match_cab(e_val).string
