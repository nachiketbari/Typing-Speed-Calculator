from django.urls import path
from typingtest import views
from typingtest.views import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    path('register/',views.user_register),
    path('login/', views.user_login),
    path('logout', views.user_logout),
    path('typing_test/', views.typing_test_view, name='typing_test'),
    path('result/', views.typing_test_result_view, name='typing_test_result'),

    
]