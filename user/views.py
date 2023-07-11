from rest_framework.views import APIView
from .serializers import UserSerializer, RequestSerializer
from rest_framework.response import Response
import jwt
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Requests,key_generator
from pymongo import MongoClient
import json
from bson.json_util import dumps
from datetime import datetime, timedelta
from rest_framework.generics import ListAPIView



# Create your views here.


class RegisterView(APIView):
    def post(self,request):
        try:
            serializer=UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({
                'message': 'User already exists'
            })


class LoginView(APIView):
    def post(self,request):
        try:
            username=request.data['username']
            password=request.data['password']     
            user=User.objects.filter(username=username).first()

            if user is None:
                raise AuthenticationFailed('Wrong username')
            if not user.check_password(password):
                raise AuthenticationFailed('Wrong password')
            
            payload={
                'username':user.username,
                'exp':datetime.utcnow()+timedelta(minutes=1440),
                'iat':datetime.utcnow()

            }
            token=jwt.encode(payload,'secret',algorithm='HS256')
            response=Response() 
            response.set_cookie(key='jwt',value=token,domain= "127.0.0.1",httponly=True, secure=False, samesite='None',max_age=86400)
            response.data={
                'jwt':token,
                'username':user.username
            }

            return response
        except Exception as e:
            print(e)


class UserView(APIView):
    def get(self,request):
        
        token=request.COOKIES.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed('NOT AUTHENTICATED')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('NOT AUTHENTICATED')

        user=User.objects.filter(username=payload['username']).first()
        serializer=UserSerializer(user)
        
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self,request):
        response=Response() 
        response.delete_cookie('jwt')
        response.data={
            'message': 'success'
        }

        return response

class show_all_requests(ListAPIView):
    queryset=Requests.objects.all()
    serializer_class=RequestSerializer


class request(APIView):
    def post(self,request):
        token=request.COOKIES.get('jwt')
        if not token:
            print("1")
            raise AuthenticationFailed('NOT AUTHENTICATED')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            print("2")
            raise AuthenticationFailed('NOT AUTHENTICATED')
        
        user=User.objects.filter(username=payload['username']).first()
        serializer=UserSerializer(user)
        Ocname=serializer.data['username']
        Oemail=request.data['email']
        Omessage=request.data['message']
    
        key=key_generator()
        Okey='O'+str(key)
        
        new_recd=Requests(rid=Okey,name=Ocname,email=Oemail,message=Omessage)
        new_recd.save()
        return Response({
            'message':'request sent successfully!'
        })
    