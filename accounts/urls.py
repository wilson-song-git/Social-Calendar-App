from django.urls import path
from .views import   Signup , Logout
from django.contrib.auth import views as auth_views
urlpatterns =[
    path('signup/' ,Signup.as_view() , name="register" ), 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', Logout, name='logout'),
]


