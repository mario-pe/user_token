from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_unique_emial(value):
        users = User.objects.filter(email=value)
        if len(users) == 0:
            return value
        raise ValidationError("Email '" + value + "' znajduje sie juz w bazie")