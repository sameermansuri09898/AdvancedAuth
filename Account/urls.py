from django.urls import path
from .views import register,login,logout,VericationOtp,ResendOtp
urlpatterns = [
    path('register/',register.as_view(),name='register'),
    path('login/',login.as_view(),name='login'),
    path('logout/',logout.as_view(),name='logout'),
    path('verifyotp/',VericationOtp.as_view(),name='verifyotp'),
    path('resendotp/',ResendOtp.as_view(),name='resendotp'),
  

]
