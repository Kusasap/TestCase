from rest_framework import routers
from django.contrib import admin
from django.urls import include, path
from index.views import QuestionApi, AnswerApi

router = routers.DefaultRouter()
router.register(r'questions', QuestionApi)
router.register(r'answers', AnswerApi)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
