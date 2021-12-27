from django.urls import path
from .views import *


urlpatterns = [
    path('', deteksi_mandiri_view, name='deteksimandiri'),

    path('get-assessments/', get_assessments, name = 'get-assessments'),
    path('save-options/', save_option, name = 'save-option'),
    path('get-assessment/<pk>', get_assessment, name = 'get-assessment'),
    path('get-assessments/<pk>', get_question, name='get-question'),
    path('create-assessment/save', create_assessment, name='create-assessment'),
    path('edit-assessment/<pk>/save', edit_assessment, name='edit-assessment'),
    path('create-assessment/<pk>/create-question/save', create_question, name='create-assessment-question'),
    path('edit-assessment/<pk>/edit-question/save', edit_question, name='edit-assessment-question'),
    path('delete-assessments/<pk>', delete_assessment, name='delete-assessment'),
    path('delete-question/<pk>', delete_question, name='delete-question'),
    path('get-assessments/<pk>/save', save_assessment, name='save-assessment'),
    path('get-assessments/<pk>/<pk2>', get_option, name='get-option'),

    path('<pk>/', quiz_view, name='quiz-view'),
    path('<pk>/data', quiz_data_view, name='quiz-data-view'),
    path('<pk>/save', save_quiz_view, name='save-quiz-view'),
    path('delete/<pk>/', delete_quiz, name='delete-quiz'),
    path('edit/<pk>/', edit_quiz, name='edit-quiz'),
    path('create-quiz/', create_quiz, name='create-quiz'),
    path('edit-questions/<pk>', edit_questions, name='edit-question' ),
    path('see-questions/<pk>', see_questions, name='see-questions'),
    path('see-questions/<pk>/delete/<pk2>', delete_questions, name='delete-questions'),
    path('see-questions/<pk>/edit/<pk2>', edit_answers, name='edit-answers'),
]
