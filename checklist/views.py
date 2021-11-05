from django.shortcuts import render
from django.utils import timezone
from .models import Task, Day, Quarantine, QuarantineDay, QuarantineTask


def checklist_home(request):
    # If there is already a running quarantine for current user.
    if request.user.is_authenticated:
        quarantine = get_current_quarantine(request.user)

        # Show list when there is already a running quarantine.
        if quarantine:
            quarantine_length = len(Day.objects.all())
            current_day = timezone.now() - quarantine.start_timestamp

            return render(request, "checklist_list.html", {
                "quarantine": quarantine,
                "quarantine_length": quarantine_length,
                "current_day": current_day.days + 1,
            })

    return render(request, "checklist_home.html", {})


def get_current_quarantine(user):
    # Get quarantine length in days.
    quarantine_length = len(Day.objects.all())
    max_start_timestamp = timezone.now() - timezone.timedelta(days=quarantine_length)

    # Get current user's already running quarantine.
    quarantines = Quarantine.objects \
        .filter(username=user.username) \
        .filter(start_timestamp__gt=max_start_timestamp)

    return quarantines[0] if quarantines else None
