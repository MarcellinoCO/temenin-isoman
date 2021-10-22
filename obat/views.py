from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Obat
from .forms import ObatForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http.response import HttpResponse
# Create your views here.
def index(request):
    obats = Obat.objects.all()
    response = {'obats': obats}
    return render(request, 'obat.html', response)

def add(request):
    context ={}
    form = ObatForm(request.POST or None)
    if form.is_valid():
        form.save()
        if request.method == 'POST':
            return HttpResponseRedirect("/obat")
    context['form']= form
    return render(request, "form.html", context)

def json(request):
    obats = Obat.objects.all()
    data = serializers.serialize('json', Obat.objects.all())
    return HttpResponse(data, content_type="application/json")
