from main.decorators import *
from django.shortcuts import render
from django.core import serializers
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from tips_and_tricks.models import TipsAndTrick
from tips_and_tricks.forms import AddForm

def index(request):
    if 'q' in request.GET:
        q = request.GET['q']
        articles=TipsAndTrick.objects.filter(title__icontains=q).order_by('id')
        if q == '':
            paginator=Paginator(articles, 3)
            articles = paginator.get_page(q)
    else:
        articles=TipsAndTrick.objects.all().order_by('id')

    if request.is_ajax():
        html = render_to_string(
            template_name="load_article.html", context={"articles": articles}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    paginator=Paginator(articles, 3)
    page_number = request.GET.get('page')
    posts_obj = paginator.get_page(page_number)
    response = {'articles': posts_obj, 'all_articles': articles}
    return render(request, 'main.html', response)


def add(request):
    form = AddForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/tips-and-tricks")
    response = {'form': form}
    return render(request, 'add.html', response)


def load_more(request):
    offset=int(request.GET['offset'])
    limit=3
    posts=TipsAndTrick.objects.all()[offset:limit+offset]
    totalData=TipsAndTrick.objects.count()
    data={}
    posts_json=serializers.serialize('json',posts)
    return JsonResponse(data={
        'posts':posts_json,
        'totalResult':totalData
    })