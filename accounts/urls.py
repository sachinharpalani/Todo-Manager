from django.urls import path
from accounts.views import registration, login, approve_account, logout

app_name = 'accounts'

urlpatterns = [
    path('register', registration, name='register'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('approve/<int:user_id>', approve_account, name='approve'),
]
