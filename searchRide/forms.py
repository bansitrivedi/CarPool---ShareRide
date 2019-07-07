from django import forms
# from django.contrib.auth.models import User
choices = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
)
class SearchRideForm(forms.Form):
    source_location = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control search-slt",'id':"searchBox",'placeholder': 'Enter Source Location'}))
    destination_location = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control search-slt",'id':"searchBoxAlt",'placeholder': 'Enter Destination Location'}))
    seat_no = forms.ChoiceField(choices=choices,widget=forms.Select(attrs={'class': "form-control search-slt",'id':"exampleFormControlSelect1",'placeholder': 'Enter Number of seats'}))

