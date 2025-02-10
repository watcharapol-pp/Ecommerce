from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse as render
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404

# Create your views here.

def cart_summary(request) :

    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {'cart': cart} )

def cart_add(request) :
    cart = Cart(request)
    if request.method == 'POST' :
    # if request.POST.get('action') == 'post' :
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity)
        cart_qty = cart.__len__()
        reponse = JsonResponse({'qty': cart_qty})
        return reponse
        # return JsonResponse({'success': True, 'message': 'Product added to cart'})
    # return JsonResponse({'success': False, 'message': 'Failed to add product to cart'})


# def cart_update(request) :
#     cart = Cart(request)
#     if request.method == 'POST':
#         product_id = int(request.POST.get('productid'))
#         quantity = int(request.POST.get('quantity'))
#         cart.update(product_id, quantity)
#         cart_qty = cart.__len__()
#         cart_total = cart.get_total() 
#         return JsonResponse({'qty': cart_qty, 'total': cart_total})

def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        try:
            # รับค่าจาก request.POST
            product_id = request.POST.get('productid')
            quantity = request.POST.get('quantity')

            # ตรวจสอบว่า product_id และ quantity ไม่เป็นค่าว่าง
            if not product_id or not quantity:
                return JsonResponse({'error': 'Missing product ID or quantity'}, status=400)

            # แปลงค่าเป็น int
            product_id = int(product_id)
            quantity = int(quantity)

            # ตรวจสอบว่า quantity มากกว่า 0
            if quantity <= 0:
                return JsonResponse({'error': 'Quantity must be greater than zero'}, status=400)

            # อัพเดทตะกร้าสินค้า
            cart.update(product_id, quantity)
            cart_qty = cart.__len__()
            cart_total = cart.get_total()
            return JsonResponse({'qty': cart_qty, 'total': cart_total})
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid input data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
        # return reponse
        

def cart_delete(request):
    if request.method == 'POST':  # Ensure it's a POST request
        cart = Cart(request)  #  Cart object
        product_id = request.POST.get('product')  # productid from the request
        quantity = int(request.POST.get('quantity', 1))  # quantity (default to 1)
        # product = get_object_or_404(Product, id=product_id)
        product = Product.objects.filter(id=product_id).first()
        cart.delete(product, quantity)
        cart_qty = cart.__len__()
        reponse = HttpResponse(product, cart_qty)
        
        return reponse

    #     return JsonResponse({'success': True, 'message': 'Product removed from cart'})
    # return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
    





