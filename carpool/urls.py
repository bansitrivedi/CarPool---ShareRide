"""carpool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path,include
from users import views as user_views
from placeRide import views as placeRide_views
from placeRide.views import MyPlacedRidesView,MyBookedRidesView
from searchRide.views import search_view,BookedRideDeleteView
from django.conf.urls import handler404, handler500,url
from payment import views as payments_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',user_views.register, name='register'),
    path('profile/',user_views.profile, name='profile'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    url(r'^paypal/',include('paypal.standard.ipn.urls')),
    url(r'^payment/',include(('payment.urls','payment'),namespace='payments')),
    # path('payment/',include('home.urls'),name='payment'),
    # path('my_booked_rides/process/',payments_views.payment_process,name='process')
    # path('my_booked_rides/done/',payments_views.payment_done,name='done')
    # path('my_booked_rides/canceled/',payments_views.payment_canceled,name='canceled')
    # Ride placing urls
    path('placeRide/',placeRide_views.placeRide, name='placeRide'),
    path('my_booked_rides/',MyBookedRidesView.as_view(template_name='placeRide/my_booked_rides.html'), name='my_booked_rides'),
    path('my_rides/',MyPlacedRidesView.as_view(template_name='placeRide/my_rides.html',date_field="journey_date"), name='my_rides'),
    path('my_rides/<int:pk>/update/', placeRide_views.RideUpdateView.as_view(), name='ride-update'),
    path('my_rides/<int:pk>/delete/', placeRide_views.RideDeleteView.as_view(), name='ride-delete'),
    path('my_rides/<int:pk>/view/', placeRide_views.RideDetailView.as_view(), name='ride-view'),

    # searching ride urls
    path('searchRide/',search_view, name='searchRide'),


    path('my_booked_rides/<int:pk>/delete/',BookedRideDeleteView.as_view(), name='booked-ride-delete'),

    # home urls
    path('',include('home.urls')),

    #for password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),

    
]
handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
