from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import  IsAuthenticated , AllowAny
from accounts import serializers
from .email import email_verify, generate_code , reset_password
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt
from django.contrib.auth import login 
from rest_framework.renderers import TemplateHTMLRenderer
from .models import User
from property.serializers import UnitSerializers
from property.models import Unit

class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self , request):
        serializer = serializers.RegisterSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # email_verify(request,user)
        return Response({"status":True , "message":"please check your mail to activate account"} , status=status.HTTP_200_OK)





#verify user by link activate
class VerifyEmail(APIView):

    serializer_class = serializers.EmailVerificationSerializer
    renderer_classes = [TemplateHTMLRenderer]
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self , request , **kwargs):
        token = request.GET.get('token')

        try :
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({ 'status' : True ,'message' :'Congratolations  Your Email is Activated'},template_name='email_verified.html',status=status.HTTP_200_OK)
            return Response({ 'status' : False ,'message' :'Error'},template_name='error404.html',status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({ 'status' : False ,'message' :'Activation Link Expired'} ,template_name='email_failed.html',status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError as identifier:
            return Response({ 'status' : False ,'message' :'Token invalid'} ,template_name='error404.html',status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):

    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        data = {
            "first_name" :user.first_name ,
 
            "email" : user.email ,
            "phone_number" : user.phone_number,
            "access" : user.get_tokens_for_user()['access'],
            "refresh" : user.get_tokens_for_user()['refresh'],
        }
        return Response({
            'status': True, "message": 'Login successfully' ,  "data":data
        }, status=status.HTTP_200_OK)

 

class ChangePasswordView(generics.GenericAPIView):
    authentication_classes = (JWTAuthentication,)  
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PasswordChangeSerializer


    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():   
            user = request.user
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            confermation_password = request.data.get('confermation_password')
            if confermation_password != new_password :
                return Response({'status' : False,'message': 'password bot match'}, status=status.HTTP_200_OK)
            if not user.check_password(old_password):
                return Response({'status' : False,'message': 'password in correct'}, status=status.HTTP_200_OK)
            user.set_password(new_password)
            user.save()
            return Response({'status' : True,'success': 'Password changed'}, status=status.HTTP_200_OK)
        return Response({'status' : False,'messege': 'Password incorrect'}, status=status.HTTP_400_BAD_REQUEST)


class SendpasswordResetEmail(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = serializers.ResetPassword
    def post(self,request,format=None):
        serializer = self.get_serializer(data =request.data)
        serializer.is_valid(raise_exception=True)
        reset_password(request.data['email'])
        return Response({'status': True,'messege' : 'check your email'},status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    
    serializer_class = serializers.LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class GetUpdateProfile(APIView):   # profile of user GET and PUT
    permission_classes = [IsAuthenticated,]
    authentication_classes = (JWTAuthentication,)
    def put(self,request, *args , **kwargs):
        data={}
        try: 
            user = self.request.user
        except User.DoesNotExist:
            return Response({ 'status' : False ,'message' :'Token invalid'},status=status.HTTP_404_NOT_FOUND)
        userSerializer = serializers.UserSerializers(user,data=request.data)
        if userSerializer.is_valid() :
            userSerializer.save()
            data.update(userSerializer.data)
            # data.update(customerSerializer.data)
            return Response({'status': True,'message' :'Updated data Successfuly','data':data} ,status=status.HTTP_202_ACCEPTED)
        else :
            return Response({ 'status' : False ,'message' :'Error data '},status=status.HTTP_404_NOT_FOUND)
    def get(self, request, format=None):
        data={}
        try:
            user = self.request.user
        except User.DoesNotExist:
            return Response({ 'status' : False ,'message' :'Token invalid'},status=status.HTTP_404_NOT_FOUND)
        
        userSerializer = serializers.UserSerializers(user)
        units = Unit.objects.filter(user=user)

        
        unitserializers = UnitSerializers(units,many = True ,context={'request':self.request})

        data.update(userSerializer.data )
        return Response({'status': True,'data':data ,'unit':unitserializers.data} ,status=status.HTTP_200_OK)
    

