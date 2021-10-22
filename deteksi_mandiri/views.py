from django.shortcuts import render
from .models import *
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

class QuizListView(ListView):
	model = Quiz
	template_name = 'quizes/main.html'

@login_required(login_url = '/admin/login/')
def quiz_view(request, pk):
	quiz = Quiz.objects.get(pk=pk)
	return render(request, 'quizes/quiz.html', {'obj':quiz})

@login_required(login_url = '/admin/login/')
def quiz_data_view(request, pk):
	quiz = Quiz.objects.get(pk=pk)
	
	questions = []
	for q in quiz.get_questions():
		answers = []
		for a in q.get_answers():
			answers.append(a.text)
		questions.append({str(q) : answers})

	return JsonResponse({
		'data' : questions,
		'time' : quiz.time,
	})

@login_required(login_url = '/admin/login/')
def save_quiz_view(request, pk):
	# print(request.POST)
	if(request.is_ajax()):
		questions = []
		data = request.POST
		data_ = dict(data.lists())
		print(data)
		print(data_)

		data_.pop('csrfmiddlewaretoken')
		
		for k in data_.keys():
			print('key: ', k)
			question = Question.objects.get(text=k)
			questions.append(question)

		print(questions)

		user = request.user
		quiz = Quiz.objects.get(pk=pk)

		score = 0
		multiplier = 100/quiz.number_of_questions
		results= []
		correct_answer = None
		full = True

		for q in questions:
			a_selected = request.POST.get(q.text)
			
			if(a_selected != ""):
				truth = False
				question_answer = Answer.objects.filter(question=q)
				for a in question_answer:
					if a_selected == a.text and (not truth):
						if a.correct:
							score+=1
							correct_answer = a.text
							results.append({str(q) : {'correct_answer' : correct_answer, 'answered' : a_selected}})
							truth = True
					else :
						if a.correct:
							correct_answer = a.text
	
				if not truth:
					results.append({str(q) : {'correct_answer' : correct_answer, 'answered' : a_selected}})
	
			else :
				results.append({str(q) : 'not-answered'})
				full = False
		
		score_ = score*multiplier

		if full :
			Result.objects.create(quiz=quiz, user=user, skor=score_)

			if score_ >= quiz.required_score_to_pass:
				return JsonResponse({'passed' :"True", 'score':score_, 'results' :results, 'full': "True"})
			else :
				return JsonResponse({'passed' :"False", 'score':score_, 'results' :results, 'full' : "True"})
		else :
			return JsonResponse({'passed' :"False", 'score':score_, 'results' :results, 'full' : "False"})