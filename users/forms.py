from django import forms
# from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
# driver_choice = ['Yes','No']
class UserRegisterForm(UserCreationForm):
    gender =forms.ChoiceField(choices = GENDER_CHOICES, label='Gender', initial='', widget=forms.Select(), required=True) 
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    aadhar = forms.CharField(min_length=12,max_length=12)
    driver= forms.BooleanField(label='Check if you are driver and add licence below', required=False)
    # driver = forms.CharField(Label='Are you driver?',widget=forms.Select(choices=driver_choice))
    mobile = forms.CharField(min_length=10,max_length=10)

    licence = forms.CharField(min_length=13,max_length=13, required=False)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','gender','aadhar','mobile','email','driver','licence','password1','password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['aadhar'].widget.attrs['class'] = "number"


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False)
    mobile = forms.CharField(required=False)
    licence = forms.CharField(required=False)
    class Meta:
     model = User
     fields = ['username','email','mobile','driver','licence']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # image = forms.ImageField(required=False,label="image")
        fields = ['image']
