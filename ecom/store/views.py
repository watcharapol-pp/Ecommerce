from django.shortcuts import render
from . models import Category, Product
from django.shortcuts import get_object_or_404
# Create your views here.
# ประกาศpathตรงนี้ทีเดียวเพื่อเข้าตัวโฟลเดอร์แล้วนำพาทไปใช้ได้ทันที 
# โดยไม่ต้องเขียนโฟลเดอร์ก่อน และสามารถนำไปใช้ส่วนอื่นต่อได้เลย
def path_temp(name):
    return f'store/{name}'

def store(request):
    all_products = Product.objects.all()
    context = {
        'my_products': all_products,
    }
    return render(request, path_temp('store.html'), context)

def categories(request):
    all_categories = Category.objects.all()
    return  {'all_categories': all_categories}

def list_category(request, category_slug=None):

# filter function
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, path_temp('list_category.html'), {'category': category, 'products':products})

#inside info product
def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {'product' : product}
    return render(request, path_temp('product-info.html'), context)