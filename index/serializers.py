from rest_framework import serializers
from index.models import Answer, Question



class QuestionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text']

class AnswerALLSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id','question_id','created_at', 'answer_text','user_id']
        read_only_fields = ['id', 'created_at','user_id']

class AnswerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['user_id', 'answer_text']
        
class QuestionALLSerializer(serializers.ModelSerializer):
    answers = AnswerALLSerializer(source='answer_set', many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'created_at', 'answers']

class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'created_at']