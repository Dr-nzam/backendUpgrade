from django.urls import path
from .views import ChangePasswordAPI,registerUser,infoUser
from .views import CustomTokenObtainPairView
   

urlpatterns = [
    path('create-user/', registerUser, name='register-user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('change-password/', ChangePasswordAPI.as_view(), name='change-password'),
    path('info-user/',infoUser,name ='info-user')
]