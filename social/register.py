from django.contrib.auth import authenticate
from accounts.models import User
from rest_framework.exceptions import AuthenticationFailed
from project.settings  import SOCIAL_SECRET

cc_id ='1043438655015-9tjikv8agtt86p44ob5j45ihmvalf532.apps.googleusercontent.com'

ss_s= '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'


def register_social_user(provider, email, name):

    filtered_user_by_email = User.objects.filter(email=email)
    if filtered_user_by_email.exists():
        
        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = authenticate(
                email=email, password=SOCIAL_SECRET)
            return {
                'first_name': registered_user.first_name,
                'last_name': registered_user.last_name,
                'username' : registered_user.username,
                'email': registered_user.email,
                "access" : registered_user.get_tokens_for_user()['access'],
                "refresh" : registered_user.get_tokens_for_user()['refresh'],
                
                }
        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else :
        name_edited = str(name).split()
        newuser = User(
            email=email,
            first_name= name_edited[0],
            last_name = name_edited[1],
            username =  name ,
            is_verified = True,
        )

        newuser.set_password(SOCIAL_SECRET)
        newuser.auth_provider = provider
        newuser.save()
        new_user = authenticate(email=email, password=SOCIAL_SECRET)
        
        return {
            "first_name" :new_user.first_name ,
            "last_name" : new_user.last_name , 
            "email" : new_user.email ,
            "username" : new_user.username,
            "access" : new_user.get_tokens_for_user()['access'],
            "refresh" : new_user.get_tokens_for_user()['refresh'],
        }