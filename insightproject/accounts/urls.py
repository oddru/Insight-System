from django.urls import path
from .views import register, user_login, user_logout, user_home, dashboard, deposit_tokens, transfer_tokens, get_transactions, get_balance

urlpatterns = [
    path('', user_home, name='home'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('deposit/', deposit_tokens, name='deposit'),
    path('transfer/', transfer_tokens, name='transfer'),
    path('api/transactions/', get_transactions, name='get_transactions'),
    path('api/balance/', get_balance, name='get_balance'),
]
