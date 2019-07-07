from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.conf import settings
# Create your views here.
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from searchRide.models import BookRide
from django.views.decorators.csrf import csrf_exempt

order = None

@csrf_exempt
def payment_done(request):
    global order
    # print(order,order.fare)
    order.is_paid = True
    order.save()
    val = request.POST.get("ride_id")
   
    return render(request,'payment/done.html')

@csrf_exempt
def payment_canceled(request):

    return render(request,'payment/canceled.html')

def payment_process(request):
    global order
    val = request.POST.get("ride_id")
    # print("i am here",val)
    # print(request.body)
    ride_id  = val
    order = get_object_or_404(BookRide,id=ride_id)
    # print(order,order.fare)
    
    fare = Decimal(order.fare)
    host = request.get_host()
    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECIEVER_EMAIL,
        "amount": fare,
        "item_name": "Book Ride {}".format(order.id),
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('payment:done')),
        "currency_code":'INR',
        "cancel_return": request.build_absolute_uri(reverse('payment:cancel')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment/process.html", context)