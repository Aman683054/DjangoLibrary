from django.core.exceptions import ValidationError


def maxvaluevalidator(value):
    if 1000 < value:
        raise ValidationError("Please enter a valid entry between 0-1000 CAD")
    else:
        return value

def minvaluevalidator(value):
    if value <= 0:
        raise ValidationError("Please enter a valid entry between 0-1000 CAD")
    else:
        return value