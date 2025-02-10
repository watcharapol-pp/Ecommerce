from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model) :
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta :
        verbose_name = "Category"
        verbose_name_plural = "Categories"


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("list_category", args=[self.slug])

class Product(models.Model) :

    #fk
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product', null=True)
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, default= 'un-branded')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length= 255)
    image = models.ImageField(upload_to='static/media/images/')

    class Meta:
        verbose_name_plural = "Products"


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product_info", args=[self.slug])


