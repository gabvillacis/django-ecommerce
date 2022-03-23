from django.conf import settings
from ecommerce.apps.catalog.models import Product

class Cart:
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, qty):
        product_id = product.id

        if product_id in self.cart:
            self.cart[product_id]["qty"] = qty
        else:
            self.cart[product_id] = {"price": float(product.price), "qty": qty}

        self.save()        

    def update(self, product_id, qty):
        if product_id in self.cart:
            self.cart[product_id]["qty"] = qty
        self.save()
    
    def delete(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __len__(self):
        return sum(item["qty"] for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]        
        self.save()