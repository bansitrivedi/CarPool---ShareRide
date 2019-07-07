from django.db import models
from users.models import User
from django.conf import settings
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
pay_mode_choices=(('OFFLINE','Ofline'),('ONLINE','Online'))
seat_choices = (
    (0,0),
    (1, 1),
    (2, 2),
    (3, 3),
)
from datetime import date
from django.db.models import Q

class SearchManager(models.Manager):
    def search(self, query=None):

        qs = self.get_queryset()
        seat_no=query['seat_no']
        seat_no=int(seat_no)


        if query is not None:
            or_lookup = (Q(source_location__icontains=query['source_location']) &
                         Q(destination_location__icontains=query['destination_location'])
                        )

            qs = qs.filter(or_lookup) # distinct() is often necessary with Q lookups
            qs = qs.filter(seat_no__gte=seat_no)

        return qs

@property
def is_past_due(self):
    return date.today() > self.date
@property
def is_greater_than_current(self):
    return  self.journey_time <= datetime.datetime.now().time()

class PlaceRide(models.Model):
    # user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Username' , on_delete = models.CASCADE)
    is_booked=models.BooleanField(default=False)
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    journey_date=models.DateField()
    journey_time = models.TimeField()
    seat_no = models.IntegerField(choices=seat_choices, default=0)
    car_model = models.CharField(max_length=40)
    car_no = models.CharField(max_length=20)

    fare=models.IntegerField(validators=[ MinValueValidator(1)])

    pay_mode=models.CharField(max_length=15,
                                      choices=pay_mode_choices,
                                      default='OFFLINE')

    source_location = models.CharField(max_length=300)
    destination_location = models.CharField(max_length=300)

    def get_absolute_url(self):
        return reverse('my_rides')

    objects         = SearchManager()
