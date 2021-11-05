from django.urls import path
from .views import *


urlpatterns = [
    path('', deteksi_mandiri_view, name='deteksi-mandiri'),
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
