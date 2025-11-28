from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.TextField(default = '')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f' {self.pk} вопрос'

class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.TextField(default = '')
    answer_text = models.TextField(default = '')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'ответ от {self.user_id}'