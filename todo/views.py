from .models import Todo
from .serializers import TodoSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
