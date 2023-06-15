from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


app_name = 'accounts'

urlpatterns = [

    path('api/token/login/',views.LoginAPIView.as_view(), name = 'login'),

    path('api/token/register/' , views.RegisterView.as_view() , name = 'register') ,

    path('api/token/email-verify/',views.VerifyEmail.as_view(), name = 'verify'),

    path('api/token/change-password/', views.ChangePasswordView.as_view(), name='change-password'),

    path('api/token/logout/',views.LogoutAPIView.as_view(), name="logout"),

    path('api/token/reset-password/' , views.SendpasswordResetEmail.as_view() , name = 'reset-password') ,

    path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),

    path('api/token/profile/',views.GetUpdateProfile.as_view(), name="Profile"),


]