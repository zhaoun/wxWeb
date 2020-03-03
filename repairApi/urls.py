from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework.routers import DefaultRouter
from repairApi import views

urlpatterns = [
    path('repair/', views.RepairList.as_view()),
    path('repair/<int:pk>/', views.RepairDetail.as_view()),
    path('repair/num/', views.RepairNum.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    path('user/', views.AUser.as_view()),
    path('users/create/', views.UserCreated),
    path('repair/feedback/', views.RepairFeedbackList.as_view()),
    path('repair/feedback/<int:pk>', views.RepairFeedbackDetail.as_view()),
    path('repair/notfeedback/', views.RepairNotFeedBackList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)