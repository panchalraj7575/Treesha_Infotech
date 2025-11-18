from rest_framework import viewsets, filters
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for tasks with support for search and ordering."""

    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "priority"]
