from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Obat
from .forms import ObatForm
from django.core import serializers
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
def index(request):
    obats = Obat.objects.all()
    response = {'obats': obats}
    return render(request, 'obat.html', response)
    
def add(request):
    obats = Obat.objects.all()
    response = {'obats': obats}
    return render(request, 'form.html', response)

def add_forms(request):
    context ={}
    form = ObatForm(request.POST or None)
    if form.is_valid():
        form.save()
        if request.method == 'POST':
            return HttpResponseRedirect("/obat/add")
    context['form']= form
    return render(request, "addforms.html", context)

def delete_obat(request):
    if (request.method == "POST"):
        id = request.POST.get("id")
        Obat.objects.filter(id=id).delete()
    return HttpResponseRedirect("/obat")

def edit_obat(request):
    if (request.method == "POST"):
        id = request.POST.get("id")
        penyakit = request.POST.get("penyakit")
        penjelasan = request.POST.get("penjelasan")
        daftar_obat = request.POST.get("daftar_obat")

        obat = Obat.objects.get(id=id)
        obat.penyakit = penyakit
        obat.penjelasan = penjelasan
        obat.daftar_obat = daftar_obat
        obat.save()

    return HttpResponseRedirect("/obat")

def json(request):
    data = serializers.serialize('json', Obat.objects.all())
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def add_from_flutter(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    new_obat = Obat(**data)
    new_obat.save()
    return JsonResponse({
        "success": "New Obat Successfully Added",
    })