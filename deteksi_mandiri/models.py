from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="Duration of the Quiz in minutes")
    required_score_to_pass = models.IntegerField(
        help_text="Required score to pass the test")

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        return self.questions.all()[:self.number_of_questions]


class Question(models.Model):
    text = models.CharField(max_length=100)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="questions")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answers.all()


class Answer(models.Model):
    text = models.CharField(max_length=100)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question : {self.question.text}, Answer : {self.text}, Correct : {self.correct}"


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skor = models.FloatField()

    def __str__(self):
        return str(self.pk)
