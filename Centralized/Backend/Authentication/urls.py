from django.urls import path
from .views import RegisterUserView, LoginView, VerifyEmailView, ProfileView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='create-user'),
    path("verify/<str:uidb64>/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
