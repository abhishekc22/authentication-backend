from django.contrib.auth import authenticate
from django.shortcuts import render
from .models import *
from .serializer import Usersignuperializer,Loginseralizer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Sgnupuser(APIView):
   def post(self, request):
        try:
            serializer = Usersignuperializer(data=request.data)
            if serializer.is_valid():
                print(serializer.data,'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                
                user_data = serializer.validated_data
                user = UserManagement.objects.create(
                email=user_data.get("email"),
                username=user_data.get("username"),
                )

                user.set_password(user_data.get("password"))
                user.save()

                return Response(
                {"messages": "Account created successfully."},
                status=status.HTTP_201_CREATED,
            )
            else:
                print(serializer.errors)
        except Exception as e:
            print(e)
            return Response({"messages": "error."},
                    status=status.HTTP_501_NOT_IMPLEMENTED)
        




class Userlogin(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = Loginseralizer(data=data)
            if serializer.is_valid():
                print(serializer.data)
                email = serializer.data['email']
                password = serializer.data['password']
                
                user = authenticate(email=email, password=password)
                print(user,'??????????????')
                if user is not None:
                    return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # Serializer is not valid
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "An error occurred."}, status=status.HTTP_501_NOT_IMPLEMENTED)
        