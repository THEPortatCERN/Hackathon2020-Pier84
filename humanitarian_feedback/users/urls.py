from django.urls import path
from django.conf.urls import include, url
from rest_framework.authtoken import views as rest_views
from django.contrib.auth import views
from users.views import ActivateView, AuthTokenView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^auth-token/', AuthTokenView.as_view()),

    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),

    path('accounts/password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('accounts/activate/<str:uid>/<str:token>/', ActivateView.as_view(), name='activate'),
]
