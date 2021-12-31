from django.utils import timezone
from .models import Day, Quarantine

def get_current_quarantine(username):
    # Get quarantine length in days.
    quarantine_length = len(Day.objects.all())
    max_start_timestamp = timezone.now() - timezone.timedelta(days=quarantine_length)

    # Get current user's already running quarantine.
    quarantines = Quarantine.objects \
        .filter(username=username) \
        .filter(start_timestamp__gt=max_start_timestamp)

    return quarantines[0] if quarantines else None
