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


def get_quarantine_data(request):
    if request.method == "POST":
        body = request.POST
        if not body:
            return JsonResponse({
                "result": "error",
                "message": "Request body not found!"
            })

        username = body["username"]
        if not username:
            return JsonResponse({
                "result": "error",
                "message": "Parameter 'username' not found in request body!"
            })

        # Get quarantine reference from username.
        quarantine = get_current_quarantine(username)

        # Construct quarantine data for page data.
        quarantine_data = []
        for day in quarantine.quarantineday_set.all():
            current_day = {"id": day.id, "day": day.day_id, "tasks": []}

            for task in day.quarantinetask_set.all():
                task_data = Task.objects.get(pk=task.task_id)
                current_day["tasks"].append({
                    "id": task.task_id,
                    "title": task_data.name,
                    "description": task_data.description,
                    "done": task.is_done
                })

            quarantine_data.append(current_day)

        return JsonResponse({
            "result": "success",
            "quarantineData": quarantine_data
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
