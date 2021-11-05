from django.shortcuts import render
from django.core import serializers
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import RumahSakit, BedRequest, Wilayah
from .forms import BedRequestForm

# Create your views here.


def bed_capacity(request):
    response = {}

    # add the dictionary during initialization
    form = BedRequestForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        id = request.POST['rs_input']
        instance = form.save(commit=False)
        instance.rs = RumahSakit.objects.get(id=id)
        instance.save()
        return HttpResponseRedirect('/bed_capacity')

    response["form"] = form
    response["rumahsakit"] = RumahSakit.objects.all().values()

    return render(request, 'main/bed_capacity.html', response)


@login_required(login_url='/admin/login/')
def bed_request_admin(request):
    response = {}

    # add the dictionary during initialization
    if request.POST:
        if 'acc-del-requester' in request.POST:
            id_ = request.POST['kode-request']
            obj = BedRequest.objects.get(id=id_)

            if request.POST['kode-aksi'] == 'acc':
                rs = obj.rs
                rs.isi += 1
                rs.save()
                obj.delete()
            elif request.POST['kode-aksi'] == 'dec':
                obj.delete()

        elif 'edit-rumah-sakit' in request.POST:
            rs = RumahSakit.objects.get(id=request.POST['kode-rs'])
            rs.kapasitas = request.POST['kapasitas']
            rs.isi = request.POST['isi']
            rs.save()

        return HttpResponseRedirect('/bed_capacity/adm')

    response['requests'] = BedRequest.objects.all().values()
    return render(request, 'main/bed_request_admin.html', response)


def bed_data_json(request, id):
    data = serializers.serialize(
        'json', RumahSakit.objects.filter(kode_lokasi=id))
    return HttpResponse(data, content_type="application/json")


def get_rs_data(request, id):
    data = serializers.serialize('json', [RumahSakit.objects.get(id=id)])
    return HttpResponse(data, content_type='application/json')


@login_required(login_url='/admin/login/')
def request_data_json(request):
    data = serializers.serialize('json', BedRequest.objects.all())
    return HttpResponse(data, content_type="application/json")


@login_required(login_url='/admin/login/')
def get_request_data(request, id):
    # id di sini adalah id dari rumah sakit
    data = serializers.serialize('json', BedRequest.objects.filter(rs=id))
    return HttpResponse(data, content_type='application/json')


def wilayah_json(request):
    data = serializers.serialize('json', Wilayah.objects.all())
    return HttpResponse(data, content_type="application/json")
