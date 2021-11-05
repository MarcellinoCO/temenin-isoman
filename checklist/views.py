from django.shortcuts import render


def checklist_home(request):
    return render(request, "checklist_home.html", {})
