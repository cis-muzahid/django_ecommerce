from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Cart, Wishlist
from .forms import CartForm
from django.contrib import messages
from django.urls import reverse


# Create your views here.
class CartView(View):
    form_class = CartForm
    def get(self, request):
        carts = Cart.objects.filter(user=request.user, active=True)
        return render(request, 'cart/mycart.html', {'carts': carts} )
    
    def post(self, request, pk=None):
        try: 
            cart = get_object_or_404(Cart, user=request.POST['user'], product=request.POST['product'], active=True)
        except:
            cart = None
            pass
        
        if cart:
            cart.quantity = request.POST['quantity']
            cart.save()
            messages.success(request,  f'{cart.product} updated successfully in cart.')
            return redirect(reverse('product_details', kwargs={'product':cart.product, 
                                                                       'category': cart.product.category}))
        else:
            breakpoint()
            form = self.form_class(request.POST)        
            if form.is_valid():
                
                cart = form.save()
                messages.success(request,  f'{cart.product} added successfully in cart.')
                return redirect(reverse('product_details', kwargs={'product':cart.product, 
                                                                    'category': cart.product.category}))
            else:
                messages.error(request, form.errors)
                return render(request, 'cart/mycart.html')
    
class WishlistView(View):
    def get(self, request):
        return render(request, 'cart/wishlist.html')
    
    def post(self, request, pk=None):
        pass
        return render(request, 'cart/wishlist.html')
    

class DeleteView(View):
    def get(self, request, pk, action):
        if action == 'cart':
            cart = Cart.objects.get(pk=pk)
            cart.active=False 
            cart.save()
            return redirect('cart_view')
        elif action == 'wishlist':
            wishlist = Wishlist.objects.get(pk=pk)
            wishlist.active=False 
            wishlist.save()
            return redirect('wishlist_view')
