import django.forms as forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)
