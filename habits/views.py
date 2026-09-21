from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Владелец видит свои, остальные пользователи видят только публичные
        if self.request.user.is_staff:
            return Habit.objects.all()
        return Habit.objects.filter(user=self.request.user) | Habit.objects.filter(is_public=True)
