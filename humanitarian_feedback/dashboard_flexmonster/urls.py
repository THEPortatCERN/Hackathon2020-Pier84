from django.conf.urls import url
from . import views

urlpatterns = [url(r'$', views.dashboard_with_pivot, name='dashboard_with_pivot'),
               url(r'data$', views.pivot_data, name='pivot_data', ),
              ]
