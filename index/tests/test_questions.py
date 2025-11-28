import pytest
from rest_framework.test import APIClient
from index.models import Question

@pytest.mark.django_db
def test_create_question():
    client = APIClient()

    payload = {
        "question_text": "Новый тестовый вопрос"
    }

    response = client.post("/questions/", payload, format='json')

    # Проверка ответа API
    assert response.status_code == 201
    assert "question_text" in response.data
    assert response.data["question_text"] == payload["question_text"]

    # Проверка, что запись появилась в базе
    assert Question.objects.count() == 1
    q = Question.objects.first()
    assert q.question_text == payload["question_text"]
