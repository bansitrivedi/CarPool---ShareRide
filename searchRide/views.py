from django.shortcuts import render
from django.shortcuts import render,redirect
from django.core.mail import send_mail #for sending mails
from django.conf import settings
from django.contrib import messages
# search.views.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from itertools import chain
from django.urls import reverse_lazy
from django.views.generic import ListView
from placeRide.models import PlaceRide
from .forms import SearchRideForm
from searchRide.models import BookRide
from users.models import User
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail #for sending mails
from django.conf import settings

seat_no = 0
user = str()
user1 = str()
@login_required
def search_view(request):
    global seat_no
    global user,user1
    form=SearchRideForm(request.POST or None)

    if request.method=='POST' and 'book_button' in request.POST:
        ride_id=request.POST.get('ride_id')
        ride_placer_user=PlaceRide.objects.get(pk=ride_id).user
        ride_placer=User.objects.get(username=ride_placer_user)
        place_ride_id=PlaceRide.objects.get(pk=ride_id)
        place_ride_id.is_booked=not place_ride_id.is_booked
        place_ride_id.is_booked=True

        if place_ride_id.seat_no >= int(seat_no) and request.user==user:
            value1=place_ride_id.seat_no #for taking fare initial value of seats
            place_ride_id.seat_no=int(place_ride_id.seat_no)-int(seat_no)
            place_ride_id.save() #saving the changes back to db
            value2=place_ride_id.seat_no #for taking fare updated value of seats
            fare=place_ride_id.fare*(value1-value2)
            data=BookRide.objects.create(ride_placer=ride_placer,ride_acceptor=request.user,ride_id=place_ride_id,number_of_seats=int(seat_no),fare=fare)
            seat_booked = str(seat_no)

            #More data fetch for :- mail
            mobile = request.user.mobile
            email = request.user.email
            username = request.user.username  #email,mobile username of user
            contact_driver=ride_placer_user.mobile   #mobile of driver

            journey_date=PlaceRide.objects.get(pk=ride_id).journey_date
            journey_time=PlaceRide.objects.get(pk=ride_id).journey_time
            source_location=PlaceRide.objects.get(pk=ride_id).source_location
            destination_location=PlaceRide.objects.get(pk=ride_id).destination_location
            car_no = PlaceRide.objects.get(pk=ride_id).car_no
            car_model =PlaceRide.objects.get(pk=ride_id).car_model



            #Converting some data to string for mail message
            jd  = journey_date.strftime('%d-%m-%Y')
            jt =  journey_time.strftime("%H:%M")
            driver_mob = str(contact_driver)
            pass_mob = str(mobile)

            price = str(fare)


            #Sending ride details ---- (MAil)
            subject='Ride Booked Successfully'
            message='Congratulations!! Your ride is booked :)\n-: Both ride hoster and passenger are verified by QuickPool team, be assured!! :- \n______________________________________\nPassenger name: '+request.user.first_name+" "+request.user.last_name+ " "+'('+username+')' + '\nRide hoster name: '+ ride_placer.first_name+" "+ride_placer.last_name+' '+'('+ride_placer.username+')' +'\nJourney Date and time: ' + jd + ' , ' + jt + '\nSource: '+source_location + '\nDestination: '+ destination_location + '\nTotal seats booked: '+seat_booked+ '\nTotal fare: '+ price + '\n\nRide Placer Contact No.:'+ driver_mob +'\nPassenger Contact No.:'+pass_mob+'\n_________\nCar Details\nRegistration no: '+car_no+'\nCar model: '+car_model
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,ride_placer.email]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request,f'Ride has been booked!')
            return redirect('home')
        else:
            messages.warning(request,f'sorry ride is not available!')
            return redirect('home')




    if form.is_valid():
        seat_no = form.cleaned_data['seat_no']
        user = request.user
        user1 = user
        rides = PlaceRide.objects.search(form.cleaned_data)
        form=SearchRideForm()

    else:
        rides = None
    return render(request, "searchRide/search.html",
            {"form": form, "ride_list": rides,'user1':user1,"seat_no":seat_no})

# def bookRide_view(request):

booked_seat_no = 0
placed_seat_no = 0
ride = None
class BookedRideDeleteView(LoginRequiredMixin,DeleteView):

     model = BookRide
     success_url = reverse_lazy('my_booked_rides')

     def get_object(self, queryset=None):
        global booked_seat_no,placed_seat_no,ride
        obj = super(BookedRideDeleteView, self).get_object()
        booked_ride = obj.ride_id
        booked_seat_no = obj.number_of_seats
        ride_id = booked_ride.id

        ride = PlaceRide.objects.get(pk=ride_id)
        placed_seat_no = ride.seat_no
        # print("**************************************************************************************************************8")
        # ride_id = ride.id
        # number_of_seats = obj.number_of_seats
        # seat_no = PlaceRide.objects.get(id = ride_id)
        # seat_no = int(seat_no) - int(number_of_seats)
        # ride.save()


        # user = self.request.user
        # username = user.username
        # email = user.email
        # subject='You cancelled your ride'
        # # message='You cancelled your placed ride\n'+'Your ride was on: '+str(self.object.journey_date)+ ' , '+self.object.journey_time.strftime("%H:%M")+'\nFrom: '+source_location+'\nTo: '+self.object.destination_location
        # message = 'Hi' + str(booked_ride_id)
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [email]
        # send_mail( subject, message, email_from, recipient_list )

        return obj
     def delete(self, request, *args, **kwargs):
       response = super(BookedRideDeleteView, self).delete(request, *args, **kwargs)
       ride.seat_no = booked_seat_no + placed_seat_no

       ride.save()
       driver = ride.user
       driver_mail = driver.email





       user = self.request.user
       username = user.username
       email = user.email
       subject='You cancelled your booked ride.'
       message='You cancelled your booked ride\n'+'Your ride was on: '+str(ride.journey_date)+ ' , '+str(ride.journey_time)+'\nFrom: '+ride.source_location+'\nTo: '+ride.destination_location + '\n\nThank you for using our service! You can book other rides:)'

       email_from = settings.EMAIL_HOST_USER
       recipient_list = [email]
       send_mail( subject, message, email_from, recipient_list )


       subject1 = 'Ride acceptor cancelled ride'
       message1='Sorry! Ride acceptor cancelled ride\n'+'The ride was on: '+str(ride.journey_date)+ ' , '+str(ride.journey_time)+'\nFrom: '+ride.source_location+'\nTo: '+ride.destination_location + '\n\nTotal seats cancelled: '+ str(booked_seat_no) + '\nSorry for inconvenience caused, you can wait for others to book.'
       email_from = settings.EMAIL_HOST_USER
       recipient_list1 = [driver_mail]
       send_mail( subject1, message1, email_from, recipient_list1 )
       return response
