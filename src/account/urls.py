from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('contact', views.ContactUs.as_view(), name='contact-us'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.LogOut.as_view(), name='logout'),
    path('profile', views.MyProfile.as_view(), name='profile'),
]
