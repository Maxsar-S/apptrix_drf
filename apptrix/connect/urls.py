from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('api/clients/create', views.UserCreate.as_view()),
    path('api/clients/<int:pk>/match', views.UserMatch.as_view()),
    path('api/list', views.UserList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
