from django.conf import settings
from django.views import View
from django.template.loader import get_template
from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.core.mail import EmailMessage
from users.forms import CustomUserCreationForm
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics
from .tokens import account_activation_token


class AuthTokenView(ObtainAuthToken, generics.GenericAPIView):
    """
    Obtain an authorization token. This should then be passed as a header to every request in the format: 'Token [token]' where [token] is the authorisation token.
    """
    pass


User = get_user_model()
class ActivateView(View):
    def get(self, request, uid, token):
        uid_decoded = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid_decoded)
        context = {
          'form': AuthenticationForm(),
          'message': 'Registration confirmation error . Please click the reset password to generate a new confirmation email.'
        }
        if user is not None and account_activation_token.check_token(user, token):
            # Activate user
            user.is_active = True
            user.save()
            context["message"] = 'Email confirmed successfully, please login.'
            #login(request, user)

        return render(request, 'registration/login.html', context)
