from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics , filters , status 
from rest_framework.permissions import  IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Unit
from .serializers import UnitSerializers
from django.shortcuts import get_object_or_404




class UnitList(generics.ListCreateAPIView):
    queryset = Unit.objects.filter(is_approved =True)
    serializer_class = UnitSerializers
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,) 
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = UnitSerializers(queryset, many=True , context={'request':self.request})
        return Response({'status': True,'message': 'succes' , 'data' :serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data ,context={'request':self.request} )
        serializer.is_valid(raise_exception=True)
        serializer.save(self.request.user)     
        return Response(serializer.data)  
    


class UnitSearchView(generics.ListCreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializers
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,) 

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['price']
    search_fields = ['title','city','governorate', 'type_property', 'price']

    def get_queryset(self):
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        queryset = super().get_queryset()
        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset





class AddOrDeleteLikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        unit = get_object_or_404(Unit,id=request.data['unit_id'])

        if self.request.user  not in unit.favourite.all():
            unit.favourite.add(self.request.user)
            return Response({'status': True,'message': 'added successfuly'}, status=status.HTTP_200_OK)
        else:
            unit.favourite.remove(request.user)
            return Response({'status': True,'message': 'unit removed from favourite'}, status=status.HTTP_200_OK)
