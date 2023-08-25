from django.utils import timezone
from rest_framework.serializers import ValidationError


class EventValidator:
    def __init__(self, time_startted="time_started", time_finished="time_finished"):
        self.time_started = time_startted
        self.time_finished = time_finished

    def __call__(self, attrs):
        if attrs[self.time_finished] < attrs[self.time_started]:
            raise ValidationError("Время завершения не может быть раньше времени начала.", code="duration error")
        if attrs[self.time_started] < timezone.now():
            raise ValidationError("Время начала должно быть больше текущего.", code="time start error")
