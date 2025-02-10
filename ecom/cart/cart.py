from decimal import Decimal
from store.models import Product

class Cart() :
    
    def __init__(self, request) :
    
    # return user - obtain his/her existing session
        self.session = request.session
        cart = self.session.get('session_key')

# new usesr genarate a new session สร้างเซนชันใหม่
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity) :
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
        else :
            self.cart[product_id] = {'price': str(product.price), 'quantity': quantity}


        self.session.modified = True

    def __len__(self) :

        return sum(item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        all_pd_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_pd_ids)
        
        import copy

        cart = copy.deepcopy(self.cart)

        for product in products :
            cart[str(product.id)]['product'] = product
        

        for item in cart.values() :
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['quantity']
            yield item


    def get_total(self) :
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def delete(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] <= quantity:
                del self.cart[product_id]
        else :
            self.cart[product_id]['quantity'] = self.cart[product_id]['quantity'] - quantity
            self.session.modified = True

    def update(self, productid, quantity) :
        product_id = str(productid)
        product_quantity = quantity
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = product_quantity
        self.session.modified = True
           
