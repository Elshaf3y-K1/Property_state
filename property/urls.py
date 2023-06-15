from django.urls import path
from . import views


urlpatterns = [

    path('unit/',views.UnitList.as_view(), name = 'unit'),
    path('search/' , views.UnitSearchView.as_view() , name = 'search'),
    path('likes/', views.AddOrDeleteLikeView.as_view() , name = 'likes') ,
      
]