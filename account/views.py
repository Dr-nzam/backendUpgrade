from django.shortcuts import render
from rest_framework.response import Response
from .serializer.serializer_in import UserSerializer,ChangePasswordSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView
from evaluation.models import Participe

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registerUser(request):
    user = request.user
    if user.is_admin:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"message":"vous n'est pas autorise a faire cette action"}, status=status.HTTP_400_BAD_REQUEST)


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
    

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def infoUser(request):
    try:
        user = CustomUser.objects.get(id = request.user.id)
        serializer = UserSerializer(user).data
        serializer["etat"] = 'connecté'
        return Response(serializer, status=status.HTTP_200_OK)
    except:
        return Response("invalide token", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listeUser(request):
    user = request.user
    if user.is_admin:
        userBD = CustomUser.objects.all()
        serializer = UserSerializer(userBD, many = True).data
        return Response (serializer, status =status.HTTP_200_OK)
    else:
        return Response({"messsage":"Vous n'avez pas les autorisations necessaire"},
                         status=status.HTTP_400_BAD_REQUEST)
