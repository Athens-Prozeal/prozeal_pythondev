from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_worker_age(date):
    current_date = timezone.now().date()
    age = current_date.year - date.year - ((current_date.month, current_date.day) < (date.month, date.day))
    if age < 14:
        raise ValidationError('Age must be at least 14 years old.')
    
    return date
