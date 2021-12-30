from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Task, Day, Quarantine, QuarantineDay, QuarantineTask
from .utils import *


@csrf_exempt
def checklist_home(request):
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


@csrf_exempt
def start_quarantine(request):
    if request.method != "POST":
        return JsonResponse({"result": "error", "message": "Must use POST method!"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"result": "error", "message": "Not yet authenticated!"}, status=403)

    username = request.user.username

    # Get quarantine reference from username.
    quarantine = get_current_quarantine(username)
    if quarantine:
        return JsonResponse({"result": "error", "message": f"A running quarantine for {username} exists!"}, status=409)

    quarantine = Quarantine(username=username)
    quarantine.save()

    days = Day.objects.all()
    for day in days:
        quarantine_day = QuarantineDay(quarantine=quarantine, day=day)
        quarantine_day.save()

        tasks = day.tasks.all()
        for task in tasks:
            quarantine_task = QuarantineTask(day=quarantine_day, task=task)
            quarantine_task.save()

    return JsonResponse({"result": "success"}, status=200)


@csrf_exempt
def get_quarantine_data(request):
    if request.method != "POST":
        return JsonResponse({"result": "error", "message": "Must use POST method!"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"result": "error", "message": "Not yet authenticated!"}, status=403)

    username = request.user.username

    # Get quarantine reference from username.
    quarantine = get_current_quarantine(username)

    if not quarantine:
        return JsonResponse({"result": "error", "message": f"No quarantine data for user {username}!"}, status=404)

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
        "quarantineStart": quarantine.start_timestamp,
        "quarantineData": quarantine_data
    }, status=200)
