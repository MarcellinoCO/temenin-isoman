from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Task, Day, Quarantine, QuarantineDay, QuarantineTask


def checklist_home(request):
    # If there is already a running quarantine for current user.
    if request.user.is_authenticated:
        quarantine = get_current_quarantine(request.user.username)

        # Show list when there is already a running quarantine.
        if quarantine:
            quarantine_length = len(Day.objects.all())
            current_day = timezone.now() - quarantine.start_timestamp

            quarantine_days = quarantine.quarantineday_set.all()

            return render(request, "checklist_list.html", {
                "quarantine": quarantine,
                "quarantine_days": quarantine_days,
                "quarantine_length": quarantine_length,
                "current_day": current_day.days + 1,
            })

    return render(request, "checklist_home.html", {})


def get_quarantine_days(request):
    if request.method == "POST":
        if not request.POST.lists():
            return JsonResponse({
                "result": "error",
                "message": "Request body not found!"
            })

        body = dict(request.POST.lists())
        username = body["username"]

        if not username:
            return JsonResponse({
                "result": "error",
                "message": "Parameter 'user' not found in request body!"
            })
        username = username[0]

        quarantine = get_current_quarantine(username)
        quarantine_days = [
            data for data in quarantine.quarantineday_set.values()]

        return JsonResponse({
            "result": "success",
            "quarantineDays": quarantine_days
        })
    else:
        return JsonResponse({
            "result": "error",
            "message": "Only accepting POST request!"
        })


def get_current_quarantine(username):
    # Get quarantine length in days.
    quarantine_length = len(Day.objects.all())
    max_start_timestamp = timezone.now() - timezone.timedelta(days=quarantine_length)

    # Get current user's already running quarantine.
    quarantines = Quarantine.objects \
        .filter(username=username) \
        .filter(start_timestamp__gt=max_start_timestamp)

    return quarantines[0] if quarantines else None
