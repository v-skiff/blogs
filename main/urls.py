from django.urls import path
from .views import IndexView, profile, BPLoginView, BPLogoutView

app_name = 'main'
urlpatterns = [
    path('accounts/logout/', BPLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', BPLoginView.as_view(), name='login'),
    path('', IndexView.as_view(), name='index'),
]