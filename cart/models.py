from django.db import models

from store.models import Product, Variation

# Create your models here.
class Cart(models.Model):
    # that cart_id use session id from cookies section in the browser
    cart_id=models.CharField(max_length=250,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id


class Cart_Item(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation,blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.product
    
    def sub_total(self):
        return self.product.price * self.quantity