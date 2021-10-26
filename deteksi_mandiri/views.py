from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from main.decorators import allowed_users


#function for render main,html and display quiz object
def deteksi_mandiri_view(request):
    quiz = Quiz.objects.all()

    #return render
    return render(request, 'quizes/main.html', {'quizs' : quiz})


#display current quiz
# @allowed_users(allowed_roles=['common_user', 'fasilitas_kesehatan', 'admin'], path='/deteksi-mandiri/',message='You need login to start this assessment!')
def quiz_view(request, pk):
    if pk == 'delete-quiz' :
        quiz = Quiz.objects.all()

        return delete_quiz(request)
    else:
    
        quiz = Quiz.objects.get(pk=pk)

        #return render
        return render(request, 'quizes/quiz.html', {'obj': quiz})


#display all quiz questions and quiz answer
def quiz_data_view(request, pk):

    #getting all quiz object
    quiz = Quiz.objects.get(pk=pk)

    #variable for accomodate question text
    questions = []

    #looping questions
    for q in quiz.get_questions():
        
        answers = []

        #looping answer
        for a in q.get_answers():

            #appen answer to the list
            answers.append(a.text)

        #append question to the list
        questions.append({str(q): answers})

    #return JsonResponse
    return JsonResponse({'data': questions, 'time': quiz.time})


#function for calculationg quiz score for user and save it into Result
def save_quiz_view(request, pk):
    
    if(request.is_ajax()):

        #state variables for accomodate question object
        questions = []
        data = dict(request.POST)
        data.pop('csrfmiddlewaretoken')

        #looping data.keys for getting question object
        for k in data.keys():

            #append question object to questions
            question = Question.objects.get(text=k)
            questions.append(question)

        #state variables for calculatin gsocre
        score = 0
        full_score = 0
        results = []
        correct_answer = None
        full = True

        #looping questions
        for q in questions:

            #get user anwer 
            a_selected = request.POST.get(q.text)

            #executed when user answer the question
            if(a_selected != ""):
                
                #question_answer is all answer for each question
                truth = False
                max_score = 0
                question_answer = Answer.objects.filter(question=q)
                
                #looping questions_answer
                for a in question_answer:
                    
                    #check if question answer is equal with a.text and user haven't answer the question correctly
                    if a_selected == a.text and (not truth):
                        
                        #if a is correct answer, initialize correct_answer with a
                        if a.correct:
                            truth = True
                            correct_answer = a.text
                            results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})

                    #executed if user anser not equal with a.text or user have answer the question correctly
                    else:

                        #if a corect, initialize correct_answer with a.text
                        if a.correct:
                            correct_answer = a.text


                    #initialize max_score if a.poin is greater than max_score
                    if a.poin > max_score :
                        max_score = a.poin

                    #add score with a.poin
                    score += a.poin

                #xecuted if user haven't answer the question correctly
                if not truth:
                    results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})

            #excecuted if user doesn't answer the question 
            else:
                results.append({str(q): 'not-answered'})
                full = False

        #get user object and quiz object
        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        #executed if user full_score == 0
        if full_score!=0:
            score = round(score/full_score, 2)
        
        #executed if full_score != 0
        else :
            score = 0

        #if user answer all question, create Result onject and send data using JsonResponse
        if full:
            Result.objects.create(quiz=quiz, user=user, result_score=score)

            if score >= quiz.required_score_to_pass:
                return JsonResponse({'quiz': quiz.name, 'passed': "True", 'score': score, 'results': results, 'full': "True"})
        
            else:
                return JsonResponse({'quiz': quiz.name, 'passed': "False", 'score': score, 'results': results, 'full': "True"})
        
        #if not, state full as false and send data
        else:
            return JsonResponse({'quiz': quiz.name, 'passed': "False", 'score': score, 'results': results, 'full': "False"})


# handling log in form and authenticate someone as a user
def delete_quiz(request):
    quizs = Quiz.objects.all()

    # excecuted when user submiting form
    if request.method == 'POST':
        # print(request.POST)
        # # authenticating user based on username and password
        quiz_name = request.POST['quiz']
        quiz_obj = Quiz.objects.filter(name=quiz_name)

        print(quiz_name)
        print(quiz_obj)

        # # executed when user if valid
        # if quiz_obj is not None:
        #     quiz_obj.delete()
        #     messages.success(request, '{quiz_name} has been deleted!')

        #     return redirect('/delete-quiz/')

        # # excecuted when user is not valid
        # else:
            # messages.success(request, 'Choose the quiz name that want to be deleted!')
        return redirect('/deteksi-mandiri/delete-quiz/')

    # rendering login.html
    else:
        print("else")
        return render(request, 'quizes/deletequiz.html', {'quizs' : quizs})