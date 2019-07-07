from django.shortcuts import render,redirect

from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail #for sending mails
from django.conf import settings
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request,f'Account has been created for {username} !')
            subject='Registration Successful'
            message = 'Thank you for registering with us !! \nWe welcome you to QuickPool community!! \nYour username is: '+ username
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html',{'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
      u_form = UserUpdateForm(request.POST,instance=request.user)
      p_form = ProfileUpdateForm(request.POST,request.FILES, instance = request.user.profile)

      if u_form.is_valid() and p_form.is_valid():
          u_form.save()
          p_form.save()

          messages.success(request,f'Account Updated !')
          return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {

      'u_form': u_form,
      'p_form' : p_form,
    }
    return render(request, 'users/profile.html',context)
