from django import forms
# from django.contrib.auth.models import User
from .models import PlaceRide
import datetime

seat_choices = (
    (1, 1),
    (2, 2),
    (3, 3),
)
pay_mode_choices=(('OFFLINE','Offline'),('ONLINE','Online'))
class PlaceRideForm(forms.ModelForm):

    journey_date=forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    journey_time=forms.TimeField(input_formats=['%I:%M %p'],widget=forms.TimeInput(attrs={'id':'datetimepicker3'}))
    seat_no = forms.ChoiceField(choices = seat_choices, label='Enter available seat/Number of seats', initial='0', widget=forms.Select(), required=True)
    car_model = forms.CharField()
    car_no = forms.CharField()
    fare = forms.IntegerField(label='Enter the amount per seat in Rs.')
    pay_mode=forms.ChoiceField(help_text='Note: If you are choosing online mode, make sure you have paypal account with your registered mail',
                                      choices=pay_mode_choices,
                                      )

    source_location = forms.CharField(widget=forms.TextInput(attrs={"id":"searchmapBox"}))
    destination_location = forms.CharField(widget=forms.TextInput(attrs={"id":"searchmapBox2"}))
    class Meta:
        model = PlaceRide

        fields = ['journey_date','journey_time','seat_no','car_model','car_no','fare','pay_mode','source_location','destination_location']

        exclude = ['user','is_booked']
    def clean_journey_time(self):
        my_date = self.cleaned_data['journey_date']
        my_time = self.cleaned_data['journey_time']
        print(my_time)
        my_date_time = ('%s %s' % (my_date, my_time))
        my_date_time = datetime.datetime.strptime(my_date_time, '%Y-%m-%d %H:%M:%S')
        print(my_date_time)
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(current_time)
        if datetime.datetime.now() >= my_date_time:
                raise forms.ValidationError(u'Wrong Date or Time! "%s"' % my_date_time)
        return my_time


class UpdateRideForm(forms.ModelForm):

    journey_date=forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    journey_time=forms.TimeField(input_formats=['%I:%M %p'],widget=forms.TimeInput(attrs={'id':'datetimepicker3'}))
    seat_no =forms.ChoiceField(choices = seat_choices, label='Enter available seat/Number of seats', initial='', widget=forms.Select(), required=True)
    car_model = forms.CharField()
    car_no = forms.CharField()
    fare = forms.IntegerField(label='Enter the amount per seat in Rs.')
    pay_mode=forms.ChoiceField(help_text='Note: If you are choosing online mode, make sure you have paypal account with your registered mail',
                                      choices=pay_mode_choices,
                                      )

    source_location = forms.CharField(widget=forms.TextInput(attrs={"id":"searchmapBox"}))
    destination_location = forms.CharField(widget=forms.TextInput(attrs={"id":"searchmapBox2"}))
    class Meta:
        model = PlaceRide

        fields = ['journey_date','journey_time','seat_no','car_model','car_no','fare','pay_mode','source_location','destination_location']

        exclude = ['user','is_booked']
