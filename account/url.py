from django.urls import path
from .views import ChangePasswordAPI,registerUser,infoUser
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenBlacklistView
   

urlpatterns = [
    path('account/create-user/', registerUser, name='register-user'),
    path('account/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('account/logout/',logout, name='token_blacklist'),
    path('account/change-password/', ChangePasswordAPI.as_view(), name='change-password'),
    path('account/info-user/',infoUser,name ='info-user')
]