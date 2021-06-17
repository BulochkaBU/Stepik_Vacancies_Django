from typing import Union
from django import template

register = template.Library()


@register.filter()
def application(number: Union[int, str], args: str = 'отклик,отклика,откликов'):
    nom_sing, gen_sing, gen_plur = args.split(',')
    number = abs(int(number))

    if 10 <= number % 100 <= 20:
        return f'{ number } { gen_plur }'
    if number % 10 == 1:
        return f'{ number } { nom_sing }'
    if 2 <= number % 10 <= 4:
        return f'{ number } { gen_sing }'
    return f'{number} {gen_plur}'
