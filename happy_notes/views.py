from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm
from django.http import JsonResponse, HttpResponse


def index(request):
   # create object of note
   form = NoteForm(request.POST or None, request.FILES or None)
   
   if request.is_ajax():
   # check if form data is valid

      if form.is_valid():
         # save the form data to model
         instance = form.save()
         return JsonResponse({
            'sender': instance.sender,
            'title': instance.title,
            'message': instance.message
         })
         
   context = {
      'form': form,
   }
   return render(request, "notes_page.html", context)

def load_notes_view(request):
   if request.is_ajax():
      notes = Note.objects.all()
      data = []
      for obj in notes:
         item = {
            'sender': obj.sender,
            'title': obj.title,
            'message': obj.message,
            'uploaded': obj.uploaded
         }
         data.append(item)
      return JsonResponse({'data':data})