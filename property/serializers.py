from rest_framework import serializers
from .models import Unit , Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class UnitSerializers(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)
    images = ImageSerializer(many=True ,read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    def get_is_liked(self , obj):
        if  isinstance(obj , Unit) :
            return obj.get_likes_for_user(self.context['request'].user)
        else :
            return False

    class Meta:
        model = Unit
        fields = ['id' , 'title','type_property' ,
                'price' ,'bedrooms' ,'bathrooms' , 'propertySize',
                'number' ,'governorate','city', 'location' , 'description' ,
                'images' , 'is_liked']

    def save(self , user):

        unit = Unit(
            user = user ,
            title = self.validated_data['title'],
            type_property = self.validated_data['type_property'],
            price = self.validated_data['price'],
            bedrooms = self.validated_data['bedrooms'],
            bathrooms = self.validated_data['bathrooms'],
            propertySize = self.validated_data['propertySize'],
            number = self.validated_data['number'],
            governorate = self.validated_data['governorate'],
            city = self.validated_data['city'],
            location = self.validated_data['location'],
            description  = self.validated_data['description'],


        )
        unit.save()
        image = Image(
            unit = unit ,
            image = self.validated_data.get('image')
        )
        image.save()        
        return unit
        #serializer.save(request.user)

