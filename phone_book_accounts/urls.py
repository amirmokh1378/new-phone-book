from django.urls import path
from .views import login_view, register_view, logout_view

app_name = 'phone_book_accounts'

urlpatterns = [
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', register_view, name='register'),
]
