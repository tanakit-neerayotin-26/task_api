from django.contrib.auth.models import  User
from .models import Task
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'status', 'priority', 'created_at', 'updated_at']




