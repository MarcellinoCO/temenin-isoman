from types import new_class
from typing import final
from django.contrib.auth.models import AnonymousUser
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators import csrf
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.contrib import messages
from django.forms import inlineformset_factory
from django.core import serializers 
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import QuizForm
from .models import *

def get_assessments(request):
    assessment = AssessmentModel.objects.all()
   
    data = serializers.serialize('json', assessment)

    return HttpResponse(data, content_type='application/json')

def get_assessment(request, pk):
    assessment = AssessmentModel.objects.get(pk = pk)

    ls = []
    dc = {}

    dc["name"] = assessment.name
    dc["topic"] = assessment.topic
    dc["nomber_of_question"] = assessment.number_of_questions
    dc["required_score_to_pass"] = assessment.required_score_to_pass

    ls.append(dc)

    jsonStr = json.dumps(ls)

    # Return JsonResponse
    return HttpResponse(jsonStr, content_type='application/json')
    

def get_question(request, pk):

    # Getting all quiz object
    assessment = AssessmentModel.objects.get(pk=pk)

    # Variable for accomodate question text
    questions = []

    # Looping questions
    for q in assessment.get_questions():
   
        # Append question to the list
        questions.append({"question" : str(q), "pk" : q.pk})

    jsonStr = json.dumps(questions)

    # Return JsonResponse
    return HttpResponse(jsonStr, content_type='application/json')

def get_option(request, pk, pk2) :

    questions = QuestionModel.objects.get(pk=pk2)
 
    # Variable for accomodate question text
    answers = []

    # Looping questions
    for q in questions.get_answers():
        answers.append({"answer" : q.text, "poin" : q.poin, "correct" : q.correct, "pk" : q.pk, "question" : q.question.pk, "delete" : False})
    
    jsonStr = json.dumps(answers)

    # Return JsonResponse
    return HttpResponse(jsonStr, content_type='application/json')

@csrf_exempt
def save_assessment(request, pk):

    if request.method == "POST" :
        user_answers = json.loads(request.body)["answers"]

        ls = json.loads(request.body)["user"]
        user_username = ""
        if len(ls) > 0:
            user_username = ls[0]

        assessment = AssessmentModel.objects.get(pk = pk)
        questions = assessment.get_questions()

        score = 0
        full_score = 0
        result = []
        inc = 0
        lulus = False

        for q in questions:
            option = q.get_answers()
            result.append({})
            max_score = 0
            truth = False

            for o in option:
                if o.text == user_answers[inc]:
                    score += o.poin

                    if o.correct :
                        truth = True
                
                if o.poin > max_score :
                    max_score = o.poin
            
            full_score += max_score

            result[inc]['question'] = q.text
            result[inc]['answer'] = user_answers[inc]
            result[inc]['truth'] = truth 
            result[inc]['correct'] = truth 

            inc = inc+1

        presentase = 0
        
        if (full_score == 0) :
            presentase = 0
        else :
            presentase = round(score/full_score *100, 2)
        

        if presentase >= assessment.required_score_to_pass :
            lulus = True

        final_result = [{"assessment" : assessment.name, "score_to_pass" : assessment.required_score_to_pass , "score" : presentase, "lulus" : lulus, "result" : result}]
        
        jsonStr = json.dumps(final_result)

        user = User.objects.get(username = user_username)
        ResultModel.objects.create(assessment=assessment, user=user, result_score=presentase)

        # Return JsonResponse
        return HttpResponse(jsonStr, content_type='application/json')
    
    return HttpResponse("")

@csrf_exempt
def delete_assessment(request, pk) :

    assessment = AssessmentModel.objects.get(pk = pk) 
    assessment.delete()
    
    return HttpResponse("")

@csrf_exempt
def create_assessment(request):

    ls  = []

    if request.method == "POST" :
        name = json.loads(request.body)["name"]
        topic = json.loads(request.body)["topic"]
        number_of_question = int(json.loads(request.body)["number_of_question"])
        required_score_to_pass = int(json.loads(request.body)["required_score_to_pass"])

        assessment = AssessmentModel.objects.create(name= name, topic= topic, number_of_questions = number_of_question, required_score_to_pass = required_score_to_pass, time= 5)
        ls.append({'name' : name, 'topic' : topic, 'number_of_question' : number_of_question, 'required_score_to_pass' : required_score_to_pass, 'pk' : assessment.pk})
    
    jsonStr = json.dumps(ls)

    return HttpResponse(jsonStr, content_type='application/json')


@csrf_exempt
def edit_assessment(request, pk):

    ls  = []

    if request.method == "POST" :
        name = json.loads(request.body)["name"]
        topic = json.loads(request.body)["topic"]
        number_of_question = int(json.loads(request.body)["number_of_question"])
        required_score_to_pass = int(json.loads(request.body)["required_score_to_pass"])

        assessment = AssessmentModel.objects.get(pk = pk);

        if number_of_question > assessment.number_of_questions :
            l = assessment.number_of_questions
            for i in range(l, number_of_question) :
                QuestionModel.objects.create(text = "", assessment=assessment)
        else :
            l = assessment.number_of_questions
            data = QuestionModel.objects.filter(assessment=assessment)[number_of_question:l]

            for i in data:
                i.delete()

        assessment.name = name;
        assessment.topic = topic;
        assessment.number_of_questions = number_of_question;
        assessment.required_score_to_pass = required_score_to_pass;

        assessment.save()

        ls.append({'name' : name, 'topic' : topic, 'number_of_question' : number_of_question, 'required_score_to_pass' : required_score_to_pass, 'pk' : assessment.pk})
    
    jsonStr = json.dumps(ls)

    return HttpResponse(jsonStr, content_type='application/json')

@csrf_exempt
def create_question(request, pk):

    if request.method == "POST":
        assessment  = AssessmentModel.objects.get(pk = pk)
        data  = json.loads(request.body)["data"]

        for i in data:
            QuestionModel.objects.create(assessment= assessment, text=i)
        
    return HttpResponse("")

@csrf_exempt
def edit_question(request, pk):

    if request.method == "POST":
        assessment  = AssessmentModel.objects.get(pk = pk)
        data  = json.loads(request.body)["data"]

        for i in data:
            q = QuestionModel.objects.get(pk = int(i["pk"]))
            q.text = i["question"]
            q.save()
        
    return HttpResponse("")


@csrf_exempt
def delete_question(request, pk) :

    question = QuestionModel.objects.get(pk = pk) 
    assessment = question.assessment

    assessment.number_of_questions = assessment.number_of_questions - 1
    question.delete()
    assessment.save()
    
    return HttpResponse("")

@csrf_exempt
def save_option(request):

    if request.method == "POST" :
        data = json.loads(request.body)["data"]

        for i in data:

            nottruth = i["answer"] == '' or i["poin"] == ''

            if nottruth:
                continue

            if i["delete"]:
                            
                # Answer deleted
                try :
                    pk = i["pk"]
                    answer = AnswerModel.objects.get(pk = pk)
                    answer.delete()
                except:
                    continue

            else :
               
                try:

                    #Answer Edited
                    question = QuestionModel.objects.get(pk = i["question"])
                    answer = AnswerModel.objects.get(pk = i["pk"])
                    answer.text = i["answer"]
                    answer.poin = int(i["poin"])
                    answer.correct = i["correct"]

                    answer.save()

                except:
                    # Answer Created
                    pk = i["question"]
                    question = QuestionModel.objects.get(pk = pk)
                    answer = AnswerModel.objects.create(text = i["answer"], correct = i["correct"], question = question, poin= int(i["poin"]))
                  

    return HttpResponse("")


        

# Function for render main,html and display quiz object
def deteksi_mandiri_view(request):
    assessment = AssessmentModel.objects.all()

    # Return render
    return render(request, 'quizes/main.html', {'quizs' : assessment})


# Display current quiz
@allowed_users(allowed_roles=['common_user', 'fasilitas_kesehatan', 'admin'], path='/deteksimandiri/', message='You need login to start this assessment!')
def quiz_view(request, pk):
    if pk == 'create-quiz' :
      return create_quiz(request)
    elif pk == 'see-questions':
      return see_questions(request)

    assessment = AssessmentModel.objects.get(pk=pk)

    # Return render
    return render(request, 'quizes/quiz.html', {'obj': assessment})


# Display all quiz questions and quiz answer
@allowed_users(allowed_roles=['common_user', 'fasilitas_kesehatan', 'admin'], path='/deteksimandiri/', message='You need login to start this assessment!')
def quiz_data_view(request, pk):

    # Getting all quiz object
    assessment = AssessmentModel.objects.get(pk=pk)

    # Variable for accomodate question text
    questions = []

    # Looping questions
    for q in assessment.get_questions():
        
        answers = []

        # Looping answer
        for a in q.get_answers():

            # Append answer to the list
            answers.append(a.text)

        # Append question to the list
        questions.append({str(q): answers})

    # Return JsonResponse
    return JsonResponse({'data': questions, 'time': assessment.time})


# Function for calculationg quiz score for user and save it into Result
@allowed_users(allowed_roles=['common_user', 'fasilitas_kesehatan', 'admin'], path='/deteksimandiri/', message='You need login to start this assessment!')
def save_quiz_view(request, pk):
    
    if(request.is_ajax()):

        # State variables for accomodate question object
        questions = []
        data = dict(request.POST)
        data.pop('csrfmiddlewaretoken')

        # Looping data.keys for getting question object
        for k in data.keys():

            # Append question object to questions
            question = QuestionModel.objects.get(text=k)
            questions.append(question)

        # State variables for calculatin gsocre
        score = 0
        full_score = 0
        results = []
        correct_answer = None
        full = True

        # Looping questions
        for q in questions:

            # Get user anwer 
            a_selected = request.POST.get(q.text)

            # Executed when user answer the question
            if(a_selected != ""):
                
                # Question_answer is all answer for each question
                truth = False
                max_score = 0
                question_answer = AnswerModel.objects.filter(question=q)
                
                # Looping questions_answer
                for a in question_answer:
                    
                    # Check if question answer is equal with a.text and user haven't answer the question correctly
                    if a_selected == a.text and (not truth):
                        
                        # If a is correct answer, initialize correct_answer with a
                        if a.correct:
                            truth = True
                            correct_answer = a.text
                            results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})

                        # Add score with a.poin
                        score += a.poin

                    # Executed if user anser not equal with a.text or user have answer the question correctly
                    else:

                        # If a corect, initialize correct_answer with a.text
                        if a.correct:
                            correct_answer = a.text


                    # Initialize max_score if a.poin is greater than max_score
                    if a.poin > max_score :
                        max_score = a.poin


                full_score += max_score

                # Executed if user haven't answer the question correctly
                if not truth:
                    results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})

            # Excecuted if user doesn't answer the question 
            else:
                results.append({str(q): 'not-answered'})
                full = False

        # Get user object and quiz object
        user = request.user
        assessment = AssessmentModel.objects.get(pk=pk)

        # Executed if user full_score == 0
        if full_score!=0:
            score = round(score/full_score * 100, 2)
        
        # Executed if full_score != 0
        else :
            score = 0

        # If user answer all question, create Result onject and send data using JsonResponse
        if full:
            ResultModel.objects.create(assessment=assessment, user=user, result_score=score)

            if score >= assessment.required_score_to_pass:
                return JsonResponse({'quiz': assessment.name, 'passed': "True", 'score': score, 'results': results, 'full': "True"})
        
            else:
                return JsonResponse({'quiz': assessment.name, 'passed': "False", 'score': score, 'results': results, 'full': "True"})
        
        # If not, state full as false and send data
        else:
            return JsonResponse({'quiz': assessment.name, 'passed': "False", 'score': score, 'results': results, 'full': "False"})


# Function for delete quiz
@allowed_users(allowed_roles=['fasilitas_kesehatan', 'admin'], path='/deteksimandiri/', message='You are not authorized to see this page!')
def delete_quiz(request, pk):

    # Get object and object name
    assessment_obj = AssessmentModel.objects.get(pk=pk)
    assesment_name = assessment_obj.name

    # Delete object quiz and send message if delete opations is success
    assessment_obj.delete()
    messages.success(request, assesment_name + ' has been deleted!')
    
    # Redirect to deteksimandiri
    return redirect('/deteksimandiri/')


# Function for edit quiz
@allowed_users(allowed_roles=['fasilitas_kesehatan', 'admin'], path='/deteksimandiri/', message='You are not authorized to see this page!')
def edit_quiz(request, pk):

    # Get quiz object and create QuizForm instance
    assessment = AssessmentModel.objects.get(pk=pk)
    form = QuizForm(instance=assessment)

    # Check if methos is POST
    if request.method == 'POST':
        # Create QuizForm instance 
        form = QuizForm(request.POST, instance=assessment)

        # If form is valid, save quiz
        if form.is_valid():
        
            form.save()

            # Redirect to edit_questions
            return redirect('/deteksimandiri/edit-questions/'+pk)

        # If Form isn't valid
        else :

            # Redirect to this page again and send message
            messages.success(request, 'Fill in all fields with valid input!')
            return redirect('/deteksimandiri/edit/'+pk)

    # Render edtiquiz.html and content dictionary
    content = {'name':assessment.name , 'topic':assessment.topic, 'number_of_questions': assessment.number_of_questions, 'time':assessment.time, 'required_score_to_pass':assessment.required_score_to_pass}
    return render(request, 'quizes/editquiz.html', content)


# Function for create Quiz
@allowed_users(allowed_roles=['fasilitas_kesehatan', 'admin'], path='/deteksimandiri/', message='You are not authorized to see this page!')
def create_quiz(request):

    # Create form Quiz
    form = QuizForm()

    # If method is POST
    if request.method == 'POST':
        # Get all value from request POST
        form = QuizForm(request.POST)

        # If form is valis, save quiz and redirect to edit-question page
        if form.is_valid():
            
            form.save()
            assessment = AssessmentModel.objects.get(name=request.POST['name'])

            return redirect('/deteksimandiri/edit-questions/'+str(assessment.pk))

        # If form isn't valid, send message and redirect to this page again
        else :
            messages.success(request, 'Fill in all fields with valid input!')
            return redirect('/deteksimandiri/create-quiz/')

    # Render createquiz.html and dictionary
    return render(request, 'quizes/createquiz.html', {'form': form})


# Function for edit question
@allowed_users(allowed_roles=['fasilitas_kesehatan', 'admin'], path='/deteksimandiri/', message='You are not authorized to see this page!')
def edit_questions(request, pk):

    # Get quiz object and create inlineforsmset_factory & formset
    assessment = AssessmentModel.objects.get(pk=pk)
    questionFormSet = inlineformset_factory(AssessmentModel, QuestionModel, fields=('text', ), extra=1000, can_delete=False, max_num=assessment.number_of_questions)
    formset = questionFormSet(instance=assessment)

    # If request method is POST
    if request.method == 'POST':
        formset = questionFormSet(request.POST, instance=assessment)
        
        # If form is valid, save form and redirect to deteksi mandiri
        if formset.is_valid():
            formset.save()

            messages.success(request, 'Your action has been saved!')
            return redirect('/deteksimandiri/')
        
        # If form isn't valid , send message and redirect to this page again
        else:

            messages.success(request, 'Fill in all fields with valid input!')
            return redirect('/deteksimandiri/edit-questions'+str(pk))

    # Render editquestion.html and dictionary
    return render(request, 'quizes/editquestion.html', {'formset' : formset, 'quiz' : assessment})


# Function for see question
@allowed_users(allowed_roles=['fasilitas_kesehatan', 'admin'], path='/deteksimandiri/', message='You are not authorized to see this page!')
def see_questions(request, pk):

    # Get quiz and questions object
    quiz = AssessmentModel.objects.get(pk=pk)
    questions = quiz.get_questions()

    # Render seequestions.html and dictionary
    return render(request, 'quizes/seequestions.html', {'questions' : questions, 'quiz' : quiz})


# Function for delete question
@allowed_users(allowed_roles=['fasilitas_kesehatan', 'admin'], path='/deteksimandiri/', message='You are not authorized to see this page!')
def delete_questions(request, pk, pk2):

    # Get question object and question name
    question_obj = QuestionModel.objects.get(pk=pk2)
    question_name = question_obj.text

    # Delete question object 
    question_obj.delete()

    # Send message and redirect to see_question
    messages.success(request, question_name + ' has been deleted!')
    return redirect('/deteksimandiri/see-questions/'+str(pk))


# Function fot edit answers
@allowed_users(allowed_roles=['fasilitas_kesehatan', 'admin'], path='/deteksimandiri/', message='You are not authorized to see this page!')
def edit_answers(request, pk, pk2):

    # Get question object and create answerFormse and Formset 
    question = QuestionModel.objects.get(pk=pk2)
    answerFormSet = inlineformset_factory(QuestionModel, AnswerModel, fields=('text', 'poin', 'correct',), extra=5, can_delete=True, max_num=5)
    formset = answerFormSet(instance=question)

    # If request method is POST 
    if request.method == 'POST':

        formset = answerFormSet(request.POST, instance=question)

        # If formset is valid save formset and return message
        if formset.is_valid():
            formset.save()

            messages.success(request, 'Your action has been saved!')
            return redirect('/deteksimandiri/see-questions/' + str(pk))

        # If isn't valid, send message and go to this page again
        else :

            messages.success(request, 'Fill in all fields with valid input!')
            return redirect('/deteksimandiri/see-questions/' + str(pk) + '/edit/' + str(pk2))


    # Render editanswer.html and fictionary
    return render(request, 'quizes/editanswer.html', {'formset' : formset, 'question' : question})