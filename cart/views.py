from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Cart, Wishlist
from .forms import CartForm, WishlistForm
from django.contrib import messages
from django.urls import reverse


# Create your views here.
class CartView(View):
    form_class = CartForm
    def get(self, request):
        if request.user.id:
            try:
                try:
                    carts = Cart.objects.filter(user=request.user.id, active=True, product__name__icontains=request.GET['q']).order_by('-id')
                except:
                    carts = Cart.objects.filter(user=request.user.id, active=True).order_by('-id')
            except Cart.DoesNotExist:
                carts = None
            return render(request, 'cart/mycart.html', {'carts': carts} )
        else:
            return redirect('login_user')

    def post(self, request, pk=None):
        try:
            cart = get_object_or_404(Cart, user=request.POST['user'], product=request.POST['product'], active=True)
        except:
            cart = None
            pass

        if request.user.id:
            if cart:
                try:
                    cart.quantity += request.POST['quantity']
                except:
                    cart.quantity += 1
                cart.save()
                messages.success(request,  f'{cart.product} updated successfully in cart.')
                return redirect('cart_view')
            else:
                form = self.form_class(request.POST)
                if form.is_valid():
                    cart = form.save()
                    messages.success(request,  f'{cart.product} added successfully in cart.')
                    return redirect('cart_view')
                else:
                    messages.error(request, form.errors)
                    return render(request, 'cart/mycart.html')
        else:
            return redirect('login_user')

class WishlistView(View):
    def get(self, request):
        try:
            try:
                wishlists = Wishlist.objects.filter(user=request.user.id, active=True, product__name__icontains=request.GET['q']).order_by('-id')
            except:
                wishlists = Wishlist.objects.filter(user=request.user.id, active=True).order_by('-id')
        except Wishlist.DoesNotExist:
            wishlists = []
        return render(request, 'cart/wishlist.html', {'wishlists': wishlists})

    def post(self, request, pk=None):
        try:
            wishlist = get_object_or_404(Wishlist, user=request.POST['user'], product=request.POST['product'], active=True)
        except:
            wishlist = None

        if request.user.id:
            if wishlist:
                return redirect('wishlist_view')
            else:
                form = WishlistForm(request.POST)
                if form.is_valid():
                    wishlist = form.save()
                    messages.success(request,  f'{wishlist.product} added successfully in Wishlist.')
                    return redirect(reverse('product_details', kwargs={'product':wishlist.product,
                                                                        'category': wishlist.product.category}))
                else:
                    messages.error(request, form.errors)
                    return render(request, 'cart/wishlist.html')
        else:
            return redirect('login_user')


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
