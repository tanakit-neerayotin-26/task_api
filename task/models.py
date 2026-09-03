from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'todo', 'Todo'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
            LOW = 'low', 'Low'
            MEDIUM = 'medium', 'Medium'
            HIGH = 'high', 'High'    

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=30, 
                              choices=Status.choices,
                                default=Status.TODO)
    
    priority = models.CharField(max_length=30,
                                choices=Priority.choices,
                                default=Priority.MEDIUM)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
         return self.title

    class Meta:
         ordering = ['created_at']
