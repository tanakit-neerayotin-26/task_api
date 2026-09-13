from .serializer import  TaskSerializer, RegisterSerializer
from .models import Task
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

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

def health_check(request):
    return JsonResponse({"status":"ok"})

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                  "message": "User created successfully"
            },
            status=status.HTTP_201_CREATED)
        else:
            return Response({
                              "message": "User created unsuccessfully",
                              "errors":serializer.errors
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                        )
          
