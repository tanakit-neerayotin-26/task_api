from django.contrib.auth.models import  User
from .models import Task
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'status', 'priority', 'created_at', 'updated_at']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
     model = User
     fields= ['username', 'password']

    def create(self,validated_data):
        user = User.objects.create_user(
        username=validated_data['username'],
        password=validated_data['password']
             )
        return user




