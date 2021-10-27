from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'


@login_required(login_url='/admin/login/')
def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.html', {'quiz': quiz})


@login_required(login_url='/admin/login/')
def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)

    questions = []
    for question in quiz.get_questions():
        answers = []
        for answer in question.get_answers():
            answers.append(answer.text)
        questions.append({str(question): answers})

    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


@login_required(login_url='/admin/login/')
def save_quiz_view(request, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for key in data_.keys():
            question = Question.objects.get(text=key)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        multiplier = 100 / quiz.number_of_questions
        score = 0
        results = []
        correct_answer = None
        full = True

        for question in questions:
            answer_selected = request.POST.get(question.text)

            if answer_selected != "":
                truth = False
                question_answer = Answer.objects.filter(question=question)

                for answer in question_answer:
                    if answer_selected == answer.text and (not truth):
                        if answer.correct:
                            score += 1
                            correct_answer = answer.text
                            results.append({
                                str(question): {
                                    'correct_answer': correct_answer,
                                    'answered': answer_selected
                                }})
                            truth = True
                    else:
                        if answer.correct:
                            correct_answer = answer.text

                if not truth:
                    results.append({
                        str(question): {
                            'correct_answer': correct_answer,
                            'answered': answer_selected
                        }})

            else:
                results.append({str(question): 'not-answered'})
                full = False

        score_ = score * multiplier

        if full:
            Result.objects.create(quiz=quiz, user=user, skor=score_)

            if score_ >= quiz.required_score_to_pass:
                return JsonResponse({
                    'passed': "True",
                    'score': score_,
                    'results': results,
                    'full': "True"
                })
            else:
                return JsonResponse({
                    'passed': "False",
                    'score': score_,
                    'results': results,
                    'full': "True"
                })
        else:
            return JsonResponse({
                'passed': "False",
                'score': score_,
                'results': results,
                'full': "False"
            })
