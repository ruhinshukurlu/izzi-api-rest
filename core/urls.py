from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from core.views import *

urlpatterns = [
    path('services/', ServiceListView.as_view()),
    path('subServices/', SubServiceListView.as_view()),
    path('subServices/<int:pk>/', SubServiceDetailView.as_view()),
    path('comments/', CommentListView.as_view()),
    path('cities/', CityListView.as_view()),
    path('orders/', OrderListView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
    path('taskers/', TaskerListView.as_view()),
]
