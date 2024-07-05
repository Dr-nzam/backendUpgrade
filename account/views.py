from django.shortcuts import render
from rest_framework.response import Response
from .serializer.serializer_in import UserSerializer,ChangePasswordSerializer, RefreshTokenSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, generics,permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registerUser(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    authentication_classes = [] 

    
class ChangePasswordAPI(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# @permission_classes([IsAuthenticated])
# @api_view(['GET'])
# def infoUser(request):
#     try:
#         # Vérifier la validité du token
#         jwt_value = JWTAuthentication().get_validated_token(request)
#         user = CustomUser.objects.get(id=request.user.id)
#         serializer = UserSerializer(user).data
#         serializer["etat"] = 'connecté'
#         return Response(serializer, status=status.HTTP_200_OK)
#     except InvalidToken as e:
#         return Response({'error': 'Token invalide'}, status=status.HTTP_401_UNAUTHORIZED)
    
       
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def infoUser(request):
    try:
        print('*--**--*-*-*-*-**-*-****---*-*-*-*--*-*-')
        print(JWTAuthentication().authenticate(request))
        print('*--**--*-*-*-*-**-*-****---*-*-*-*--*-*-')
        JWTAuthentication().authenticate(request)
        user = CustomUser.objects.get(id = request.user.id)
        serializer = UserSerializer(user).data
        serializer["etat"] = 'connecté'
        return Response(serializer, status=status.HTTP_200_OK)
    except:
        return Response("invalide token", status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([IsAuthenticated])
class LogoutViewd(GenericAPIView):
    def post(self, request, *args):
        sz = RefreshTokenSerializer(data=request.data, many=False)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class LogoutViewd(APIView):
#     def post(self, request):
#         try:
#             # refresh_token = request.data["refresh_token"]
#             print("toto***************************/**/*/**/*****/*-/*-////-/-///-///*-/-")
#             token = RefreshToken("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMDI2MTk2NywiaWF0IjoxNzIwMTc1NTY3LCJqdGkiOiI5ZTY4Y2EyZTEwY2E0ODNkOTE4YTAyMzE3ZTEzNTlmOCIsInVzZXJfaWQiOjJ9.jQjSYVLYR_74glKcYEe3ohd11MN4HJtEEyUsOpOsCVI")
#             token.blacklist()
#             return Response({"msg":"successfully"}, status= status.HTTP_200_OK)
#         except Exception as e:
#             return Response (str(e), status=status.HTTP_400_BAD_REQUEST)
    