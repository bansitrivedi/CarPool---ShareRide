from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser,AbstractBaseUser

# from phonenumber_field.modelfields import PhoneNumberField
# from local flavor.forms import INPhoneNumberField


# Create your models here.
GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

class User(AbstractUser):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    aadhar_ex =RegexValidator(regex='[0-9]{12}', message="Invalid Aaadhar Number")
    aadhar = models.CharField(max_length=12,validators=[aadhar_ex],unique=True)
    driver = models.BooleanField(blank=True, null=True)
    mobile_ex = RegexValidator(regex=r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$', message="Invalid Mobile Number")
    licence_ex = RegexValidator(regex='[a-zA-Z0-9/]{13}', message="Invalid licence Number")

    mobile = models.CharField(default='0',validators=[mobile_ex],max_length=10,unique=True)
    licence = models.CharField(max_length=13,validators=[licence_ex])
    email = models.EmailField(unique=True)




class Profile(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to = 'profile_pics')

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height >300 or img.width >300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
