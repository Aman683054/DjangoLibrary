import os

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

# def profileimagevalidator(value):
#     ext = os.path.splitext(value)  # [0] returns path+filename
#
#     valid_extensions = ['.jpeg', '.jpg', '.png']
#     if not ext.lower() in valid_extensions:
#         raise ValidationError(u'Unsupported file extension.')