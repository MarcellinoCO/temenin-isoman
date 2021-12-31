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

def ajson(request):
    data = serializers.serialize('json', Obat.objects.all())
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def add_from_flutter(request):
    if (request.method == "POST"):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        penyakit = body["penyakit"]
        penjelasan = body["penjelasan"]
        daftar_obat = body["daftar_obat"]

        try:
            obat = Obat(penyakit=penyakit, penjelasan=penjelasan, daftar_obat=daftar_obat)
            obat.save()
            return HttpResponse("Successful", status=200)
        except Obat.DoesNotExist:
            print("An error occurred")
            return HttpResponse("An error occurred", status=400, content_type="text/plain")
    return HttpResponse("Must use POST Method", status=405, content_type="text/plain")