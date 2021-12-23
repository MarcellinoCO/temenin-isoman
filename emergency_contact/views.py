from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Daerah, RumahSakit
from .forms import DaerahForm, RumahSakitForm

from django.contrib import messages;

def index(request):

    list_daerah = Daerah.objects.all().values()
    list_rs = RumahSakit.objects.all().values()
    response = {'list_daerah':list_daerah, 'list_rs':list_rs}
    return render(request, "main_page.html", response)

def add_rs(request):
    list_daerah = Daerah.objects.all().values()
    list_rs = RumahSakit.objects.all().values()
    form = RumahSakitForm(request.POST or None)
    if (form.is_valid() and request.method == 'POST'):
        form.save()
        messages.success(request, 'Rumah Sakit Baru Berhasil Ditambahkan')
    
    if ((not(form.is_valid())) and request.method == 'POST'):
        messages.error(request, 'Rumah Sakit Sudah Ada')
    response = {'form': form, 'list_rs':list_rs, 'list_daerah':list_daerah}
    return render(request, 'add_rs.html', response)

def add_daerah(request):
    list_daerah = Daerah.objects.all().values()
    form = DaerahForm(request.POST or None)
    
    if (form.is_valid() and request.method == 'POST'):
        form.save()
        messages.success(request, 'Kota Baru Berhasil Ditambahkan')
    
    if ((not(form.is_valid())) and request.method == 'POST'):
        messages.error(request, 'Kota Sudah Ada')

    response = {'form': form, 'list_daerah': list_daerah}
    return render(request, 'add_daerah.html', response)

def daerah_json(request):
    data = serializers.serialize('json', RumahSakit.objects.all())
    return HttpResponse(data, content_type="application/json")

def update_rs(request, pk):
    row = RumahSakit.objects.get(id=pk)
    form = RumahSakitForm(request.POST or None, instance=row)
    
    if (form.is_valid() and request.method == 'POST'):
        messages.success(request, row.nama + " Berhasil diubah")
        form.save()
    
    if ((not(form.is_valid())) and request.method == 'POST'):
        messages.error(request, "Oops, " + row.nama + " Gagal diubah nih")
    return HttpResponseRedirect('/emergency-contact/')

def hapus_rs(request, pk):
    row = RumahSakit.objects.get(id=pk)
    messages.success(request, row.nama + " Berhasil dihapus")
    row.delete()
    return HttpResponseRedirect('/emergency-contact/')

def update_daerah(request, pk):
    row = Daerah.objects.get(id=pk)
    form = DaerahForm(request.POST or None, instance=row)
    if (form.is_valid() and request.method == 'POST'):
        messages.success(request, row.daerah + " Berhasil diubah")
        form.save()
    
    if ((not(form.is_valid())) and request.method == 'POST'):
        messages.error(request, "Oops, " + row.daerah + " Gagal diubah nih")
    return HttpResponseRedirect('/emergency-contact/add-daerah')

def hapus_daerah(request, pk):
    row = Daerah.objects.get(id=pk)
    messages.success(request, row.daerah + " Berhasil dihapus")
    row.delete()
    return HttpResponseRedirect('/emergency-contact/add-daerah')