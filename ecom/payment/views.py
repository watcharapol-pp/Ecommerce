from django.shortcuts import render
from . models import Order, ShippingAddress

# Create your views here.
def payment_process(request):
    return render(request, 'payment/payment-process.html',)

def payment_success(request):
    return render(request, 'payment/payment-success.html',)

def payment_cancel(request):
    return render(request, 'payment/payment-cancel.html',)

def payment_fail(request):
    return render(request, 'payment/payment-fail.html',)


def complete_order(request):
    pass
    # if request.method == 'POST':
    #     # Process the order completion logic here
    #     order_id = request.POST.get('order_id')
    #     # Assuming you have an Order model
    #     try:
    #         order = Order.objects.get(id=order_id)
    #         order.status = 'completed'
    #         order.save()
    #         return render(request, 'payment/checkout.html', {'order': order})
    #     except Order.DoesNotExist:
    #         return render(request, 'payment/checkout.html', {'error': 'Order does not exist'})
    # return render(request, 'payment/checkout.html')



def checkout(request):
    # user with acc - pre full
    if request.user.is_authenticated:
        try:
            shipping_add = ShippingAddress.objects.get(user=request.user.id)
            context = {
                'shipping_add': shipping_add,
            }
            return render(request, 'payment/checkout.html', context=context)
        except ShippingAddress.DoesNotExist:
            return render(request, 'payment/checkout.html', context={})
    else:
        #guest user
        return render(request, 'payment/checkout.html',)

