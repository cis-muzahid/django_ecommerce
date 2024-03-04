from django.shortcuts import render
from django.views import View

# Create your views here.
class OrderView(View):
    def get(self, request):
        return render(request, 'orders/checkout.html')

    def post(self, request, pk=None):
        breakpoint()
        return render(request, 'orders/checkout.html')
