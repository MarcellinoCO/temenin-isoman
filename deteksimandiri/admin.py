from django.contrib import admin
from .models import *

admin.site.register(ResultModel)
admin.site.register(AssessmentModel)


class AnswerInLine(admin.TabularInline):
    model = AnswerModel


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]


admin.site.register(QuestionModel, QuestionAdmin)
admin.site.register(AnswerModel)
