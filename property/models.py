from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings



class Unit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_("title") ,max_length=25)
    type_property = models.CharField(max_length=25,blank=True, null=True)
    price = models.DecimalField(max_digits=12 , decimal_places=2)
    bedrooms = models.IntegerField(_("bedrooms"))
    bathrooms = models.IntegerField(_("bathrooms"))
    propertySize = models.FloatField(_("propertySize"))
    number = models.IntegerField(_("number"))
    governorate = models.TextField(_("governorate") , null=True , blank=True)
    city = models.TextField(_("city") , null=True , blank=True)
    location = models.CharField(_("location"), max_length=1000)
    description = models.TextField(_("description") , null=True , blank=True)
    favourite = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Likes' , related_name='favourite')
    is_approved =models.BooleanField(_("is_approved") ,default=False)
    images = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True)

    def get_likes_for_user(self , user):
        answer = False
        if user in self.favourite.all():
            answer = True
        return answer


    def __str__(self):
        return str(self.title)

class Image(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')




class Likes(models.Model):
    Unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user.email)


