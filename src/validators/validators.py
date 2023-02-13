from django.core.exceptions import ValidationError


def competitor_num_validator(value):               # самодельный валидатор количества введенных пользователем конкурентов
    if value:
        if value > 3:
            raise ValidationError('выбор до трех производителей')
        return value



