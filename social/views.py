from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer,FacebookSocialAuthSerializer
from rest_framework.permissions import  IsAuthenticated , AllowAny

class GoogleSocialAuthView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response({"status":True, "message":"Account Create successfully" , "data":data}, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response({"status":True, "message":"Account Create successfully" , "data":data}, status=status.HTTP_200_OK)



