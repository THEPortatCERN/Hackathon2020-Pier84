"""humanitarian_feedback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.shortcuts import redirect

import logging
logger = logging.getLogger(__name__)

urlpatterns = [
    path(r'', TemplateView.as_view(template_name='home.html'), name='home'),
    path(r'process_output_csv', TemplateView.as_view(template_name='process_output_csv.html'), name='process_output_csv'),
    path('questions', TemplateView.as_view(template_name='add_questions.html'), name='add_questions'),
]
urlpatterns += [
    url(r'^automated-survey/', include('sms_auto_surveys.urls'), name='surveys'),
    url(r'^$', lambda r: redirect('/automated-survey/'), name='root-redirect')
]
