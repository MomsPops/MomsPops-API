from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

from .models import Account


User = get_user_model()
