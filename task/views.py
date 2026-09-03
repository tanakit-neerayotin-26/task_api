from .serializer import  TaskSerializer
from .models import Task
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)