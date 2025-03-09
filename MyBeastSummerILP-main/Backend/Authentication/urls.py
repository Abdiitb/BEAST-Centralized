from django.urls import path
from .views import LoginView, ProfileView

urlpatterns = [
    # path('create-user/', CreateUserAPIView.as_view(), name='create-user'),
    # path('verify-user/', TokenVerification.as_view(), name='token-verification'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
