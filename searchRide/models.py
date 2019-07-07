from django.db import models

from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from placeRide.models import PlaceRide
# Create your models here.


class BookRide(models.Model):
    ride_placer      = models.ForeignKey(User , on_delete = models.CASCADE,related_name='placer')
    ride_acceptor    =  models.ForeignKey(User , on_delete = models.CASCADE,related_name='acceptor')
    ride_id          = models.ForeignKey(PlaceRide,to_field='id',on_delete = models.CASCADE)
    number_of_seats  = models.IntegerField(default=1,validators=[MaxValueValidator(10), MinValueValidator(1)])
    fare             = models.IntegerField(validators=[ MinValueValidator(1)])
    is_paid          = models.BooleanField(default=False)