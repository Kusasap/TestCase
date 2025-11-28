from rest_framework.decorators import action
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from index.models import Answer, Question
from index.serializers import (
    QuestionALLSerializer,
    QuestionPostSerializer,
    AnswerALLSerializer,
    AnswerPostSerializer,
    QuestionListSerializer,
)
import logging

logger = logging.getLogger("project")


# ------------------- API ------------------- 
class QuestionApi(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self):
        if self.action == 'add_answer':
            return AnswerPostSerializer

        if self.action == 'create':
            return QuestionPostSerializer

        if self.action == 'retrieve':
            return QuestionALLSerializer

        if self.action == 'list':
            return QuestionListSerializer

        return QuestionALLSerializer

    # ---------- LIST ----------
    def list(self, request, *args, **kwargs):
        logger.info("GET /questions — получение списка вопросов")
        return super().list(request, *args, **kwargs)

    # ---------- RETRIEVE ----------
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        logger.info(f"GET /questions/{pk} — получение вопроса")
        return super().retrieve(request, *args, **kwargs)

    # ---------- CREATE ----------
    def create(self, request, *args, **kwargs):
        logger.info(f"POST /questions — создание вопроса: {request.data}")
        response = super().create(request, *args, **kwargs)
        logger.info(f"Вопрос создан: {response.data}")
        return response

    # ---------- DESTROY ----------
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        logger.info(f"DELETE /questions/{pk} — удаление вопроса")
        response = super().destroy(request, *args, **kwargs)
        logger.info(f"Вопрос {pk} (и связанные ответы) успешно удалён")
        return Response({"message": "Вопрос и ответы удалены"}, status=status.HTTP_204_NO_CONTENT)

    # ---------- ADD ANSWER ----------
    @action(
        detail=True,
        methods=['post', 'get'],
        url_path='answers',
        url_name='answer'
    )
    def add_answer(self, request, pk=None):
        if request.method == "GET":
            logger.info(f"GET /questions/{pk}/answers — проверка доступности метода")
            return Response(status=status.HTTP_200_OK)

        logger.info(f"POST /questions/{pk}/answers — попытка добавления ответа: {request.data}")

        question = self.get_object()
        serializer = AnswerPostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(question_id=question)
            logger.info(f"Ответ добавлен к вопросу {pk}: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error(f"Ошибка добавления ответа для вопроса {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ------------------- ANSWERS API -------------------
class AnswerApi(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Answer.objects.all()
    serializer_class = AnswerALLSerializer
    http_method_names = ['get', 'delete']

    # ---------- RETRIEVE ----------
    def retrieve(self, request, pk=None):
        logger.info(f"GET /answers/{pk} — получение ответа")
        response = super().retrieve(request, pk)
        logger.info(f"Ответ {pk} получен: {response.data}")
        return response

    # ---------- DELETE ----------
    def destroy(self, request, pk=None):
        logger.info(f"DELETE /answers/{pk} — попытка удаления ответа")
        response = super().destroy(request, pk)
        logger.info(f"Ответ {pk} успешно удалён")
        return Response({"message": "Ответ удалён"}, status=204)
