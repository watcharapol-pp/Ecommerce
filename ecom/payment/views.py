from django.shortcuts import render
from . models import Order, ShippingAddress, OrderItem
from cart.cart import Cart
from django.http import JsonResponse


# Create your views here.
def payment_process(request):
    return render(request, 'payment/payment-process.html',)

def payment_success(request):

    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
  
    return render(request, 'payment/payment-success.html')


def payment_cancel(request):
    return render(request, 'payment/payment-cancel.html',)

def payment_fail(request):
    return render(request, 'payment/payment-fail.html',)


def complete_order(request):
    if request.method == 'POST':
        # Process the order completion logic here
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # all - 1 shipping add
        shipping_add = (address1 + "\n" + address2 + "\n" + city + "\n" + state + "\n" + zipcode + "\n")

        cart = Cart(request)

        total_cost = cart.get_total()

        # Create order => acc user with + without shipping info
        if request.user.is_authenticated:
            order = Order.objects.create(
                full_name=name, 
                email=email,  
                shipping_address=shipping_add, 
                amount_paid=total_cost,
                user=request.user)

            order_id = order.pk
            # order.save()
        # Add order items to the order
            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id, 
                    product=item['product'], 
                    price=item['price'], 
                    quantity=item['quantity'], 
                    user=request.user)
                
                # create order => guest users without acc
        else:
            order = Order.objects.create(
                full_name=name, 
                email=email,  
                shipping_address=shipping_add, 
                amount_paid=total_cost
                )
            order_id = order.pk
            # order.save()
        # Add order items to the order
            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id, 
                    product=item['product'], 
                    price=item['price'], 
                    quantity=item['quantity'], 
                )
            
    order_success = True
    response = JsonResponse({'success': order_success})

    return response
        # Clear the cart
        # cart.clear()
        # Return a response indicating payment was successful

        # Assuming you have an Order model



def checkout(request):
    # user with acc - pre full
    if request.user.is_authenticated:
        try:
            shipping_add = ShippingAddress.objects.get(user=request.user.id)
            context = {
                'shipping_add': shipping_add,
            }
            return render(request, 'payment/checkout.html', context=context)
        except:
            return render(request, 'payment/checkout.html')
    else:
        #guest user
        return render(request, 'payment/checkout.html')
    



