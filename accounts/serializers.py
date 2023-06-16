from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
#from phonenumber_field.serializerfields import PhoneNumberField
from .validation import CustomValidation
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name' , 'email' , 'username' , 'phone_number' ]



# for REGISTERATION 

class RegisterSerialzier(serializers.ModelSerializer):
    first_name = serializers.CharField(required= True)  
    email = serializers.EmailField(required= True)
    phone_number = serializers.CharField(required= True)
    password = serializers.CharField(required= True)
    password2 = serializers.CharField(required= True)

    class Meta:
        model = User
        fields = ['id','first_name','email','phone_number','password','password2']
        read_only_fields = ['id']
        extra_kwargs={
            'password' :{'write_only':True},
            'password2' :{'write_only':True},
        } 

    def validate_password(self, attrs):
        small , capital= 0 , 0
        for i in str(attrs):
            if i.isupper():
                capital +=1
            elif i.islower():
                small +=1
        if len(str(attrs)) <= 10  or small<=3 or capital<=3:
            raise CustomValidation(_("The password must consist of more than 10 characters including 4 uppercase and 4 lowercase letters "))
        return attrs
        

    def validate_email(self , attrs):
        if self.Meta.model.objects.filter(email=attrs).exists():
            raise CustomValidation(_("Email already exist"))
        return attrs


    def validate_username(self,attrs):
        if self.Meta.model.objects.filter(username=attrs).exists():
            raise CustomValidation(_("username already exist"))
        return attrs


    def validate(self, attrs):
        if attrs["password"] != attrs["password2"] :
            raise CustomValidation(_("password didnot match"))
        return attrs


    def save(self, **kwargs):
        user = self.Meta.model(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            )
        user.set_password(self.validated_data['password'])
        user.save()
        return user



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']




class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']


    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise CustomValidation(_('Please continue your login using '+ filtered_user_by_email[0].auth_provider))
        if not user:
            raise CustomValidation(_('the Email and password incorrect'))
        if not user.is_active:
            raise CustomValidation(_('Account disabled, contact admin'))
        # if not user.is_verified:
        #     raise CustomValidation(_('Email is not verified'))
        attrs['user'] = user
        return attrs





class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128 ,min_length= 8 , required= True)
    new_password = serializers.CharField(max_length=128 ,min_length= 8 , required=True)
    confermation_password = serializers.CharField(max_length=128, min_length= 8 ,required=True)

    def validate_new_password(self , attrs):
        small , capital= 0 , 0
        for i in str(attrs):
            if i.isupper():
                capital +=1
            elif i.islower():
                small +=1
        if len(str(attrs)) <= 10  or small<=3 or capital<=3:
            raise CustomValidation(_("The password must consist of more than 10 characters including 4 uppercase and 4 lowercase letters "))
        return attrs


class ResetPassword(serializers.Serializer):
    email = serializers.EmailField(required=True , max_length=255)

    def validate_email(self , attrs):
        if User.objects.filter(email=attrs).exists():
            user = User.objects.get(email=attrs)
            return user
        else:
            raise CustomValidation(_("the Email incorrect try using anather email"))



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except :
            CustomValidation('bad_token')