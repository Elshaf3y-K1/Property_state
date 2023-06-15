from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

#from app.validation import CustomValidation
from .utils import  Util
import binascii
import os



def generate_code():
    return binascii.hexlify(os.urandom(3)).decode('utf-8')




def email_verify(request,user):
    site = get_current_site(request).domain
    relativeLink = reverse('accounts:verify')
    token = RefreshToken.for_user(user).access_token
    link = 'http://'+site+relativeLink+"?token="+str(token)
    body = 'Click Following Link to verify Email\n'+ link
    data = {
        'title':'Email verification',
        'content':'Hello '+user.username ,
        'body':body, 
        'to_email': user.email
    }
    Util.send_email(data) 
    return data

from .models import User
def reset_password(email):
    try :
        user = User.objects.get(email=email)
        code = generate_code()
        user.code = code
        user.save()
        data = {
            'title':'Reset password ',
            'body':'this code for reset password '+code , 
            'to_email': user.email
        }
        Util.send_email(data) 
        return data
    except :
        return ("the Email incorrect try using anather email")
