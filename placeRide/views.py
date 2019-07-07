from django.shortcuts import render,redirect
from django import forms
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.dates import ArchiveIndexView
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from .forms import PlaceRideForm,UpdateRideForm
from django.contrib.auth.decorators import login_required
from .models import PlaceRide
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import Http404
from django.db.models import Q
from itertools import chain
from searchRide.models import BookRide

from django.core.mail import send_mail #for sending mails
from django.conf import settings
# Create your views here.

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)


#For sending mail to placed Rides
from placeRide.models import PlaceRide

from searchRide.models import BookRide
from users.models import User

id = 0
email_passengers =[]
@login_required
def placeRide(request):

    form=PlaceRideForm(request.POST or None)
    if form.is_valid():
        post=form.save(commit=False)
        post.user=request.user
        post.save()
        messages.success(request,f'Ride has been placed!')
        return redirect('home')

    return render(request, 'placeRide/placeride_form.html', {'placeRide_form': form})


class MyPlacedRidesView(LoginRequiredMixin,ArchiveIndexView):
    template_name='my_rides.html'
    model = PlaceRide
    allow_future=True
    allow_empty=True
    context_object_name = 'my_rides'
    ordering = ['journey_date']

    def get_queryset(self):
        try:
            obj=PlaceRide.objects.filter(user=self.request.user).order_by('-journey_date')
        except ObjectDoesNotExist:
            obj=None
        return obj

class MyBookedRidesView(LoginRequiredMixin,ListView):
    template_name='my_booked_rides.html'
    model = PlaceRide
    allow_future=True
    allow_empty=True
    context_object_name = 'my_rides'


    def get_queryset(self):

        obj1=BookRide.objects.filter(ride_acceptor=self.request.user)

        if obj1.exists():
            return obj1
        else:
            return PlaceRide.objects.none()


class RideUpdateView(LoginRequiredMixin,UpdateView):
    model = PlaceRide
    form_class = UpdateRideForm
    template_name = 'placeRide/update_ride.html'

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RideDeleteView(LoginRequiredMixin,DeleteView):
     model = PlaceRide
     success_url = reverse_lazy('my_rides')

     ##---------------------------------------For sending mail----------------------------
     def get_object(self, queryset=None):
        obj = super(RideDeleteView, self).get_object()
        # if not obj.owner == self.request.user:
        #     raise Http404
        global id
        global email_passengers
        user = self.request.user
        username = user.username
        email = user.email
        ride = PlaceRide.objects.get(id=obj.id)
        id = ride.id
        source_location = ride.source_location
        subject='Hi sudhanshu'
        message='Congratulations!! Your ride is cancelled :) '+ source_location+' '+str(id)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        # send_mail( subject, message, email_from, recipient_list )

        booked_list = BookRide.objects.filter(ride_id=id)#used filter as multiple value will be returned
        for objects in booked_list:
         ride_acceptor_user = objects.ride_acceptor
         ride_acceptor=User.objects.get(username=ride_acceptor_user)
         email_passengers.append(ride_acceptor.email)
        return obj

     def delete(self, request, *args, **kwargs):
       response = super(RideDeleteView, self).delete(request, *args, **kwargs)
       user = self.request.user
       username = user.username
       email = user.email
       source_location = self.object.source_location
    #    print(email)
       subject='You cancelled your ride'
       message='You cancelled your placed ride\n'+'Your ride was on: '+str(self.object.journey_date)+ ' , '+self.object.journey_time.strftime("%H:%M")+'\nFrom: '+source_location+'\nTo: '+self.object.destination_location
       email_from = settings.EMAIL_HOST_USER
       recipient_list = [email]
       send_mail( subject, message, email_from, recipient_list )

       #Sending mail to email_passengerrs
       subject='Your ride is cancelled by ride hoster'
       message=' Your ride is cancelled by ride hoster: '+ user.first_name+" "+user.last_name +'\n Your ride was on: '+str(self.object.journey_date)+ ' , '+self.object.journey_time.strftime("%H:%M")+'\n From: '+source_location+ "\nTo: "+self.object.destination_location+'\n\nWe regret the inconvenience caused to you, You can search for other rides.'
       email_from = settings.EMAIL_HOST_USER
       recipient_list = email_passengers
       send_mail( subject, message, email_from, recipient_list )
       return response






class RideDetailView(LoginRequiredMixin,DetailView):
    model = PlaceRide
    context_object_name = 'ride'
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return PlaceRide.objects.filter(user=self.request.user)
        else:
            return PlaceRide.objects.none()
