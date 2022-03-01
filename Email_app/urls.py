from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView, name="login"),
    path('signup/', views.signupview, name="signup"),
    path('sent_email/', views.sent_email, name="sent_email"),
    path('verify/<auth_token>', views.verify, name="verify"),
    path('home/', views.home, name="home"),
   
]