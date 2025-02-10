from django.urls import path
from . import views




urlpatterns = [
    # store main
    path('', views.store, name='store'),

    #individual product ชื่อ ของproduct_infoอยุ่ตรงนี้
    path('product/<slug:product_slug>/', views.product_info, name='product_info'),

    # category
    path('search/<slug:category_slug>/', views.list_category, name='list_category'),
]
