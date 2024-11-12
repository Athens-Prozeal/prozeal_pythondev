from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_due_date(date):
    current_date = timezone.now().date()
    if date < current_date:
        raise ValidationError('Due date cannot be in the past.')

    return date
