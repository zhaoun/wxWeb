from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from repairApi import views


urlpatterns = [
    path('repair/', views.RepairList.as_view()),
    path('repair/<int:pk>/', views.RepairDetail.as_view()),
    path('repair/num/', views.GetNums),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('users/create/', views.UserCreated),
]

urlpatterns = format_suffix_patterns(urlpatterns)