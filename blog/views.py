from django.shortcuts import render, redirect
from .models import Blog
from django.views import View
from django.contrib import messages
from .forms import BlogForm

# Create your views here.
class BlogView(View):
    def get(self, request):
        blogs = Blog.objects.filter(active=True)
        return render(request, "admin/blog/blog.html", {'blogs': blogs })

    def post(self, request):
        if request.POST.get("blog"):
            action = "updat"
            blog = Blog.objects.get(id=request.POST.get("blog"))
            form = BlogForm(request.POST, request.FILES, instance=blog)
        else:
            action = "add"
            form = BlogForm(request.POST, request.FILES)

        blogs = Blog.objects.filter(active=True)
        try: 
            if form.is_valid():
                form.save()
                messages.success(request, f" Blog {action}ed successfully.")
                return redirect('admin_blog_view')
            else:
                messages.error(request, f"An error occurred while {action}ing blog : ", form.errors)
        except Exception as e:
            messages.error(request, f"An error occurred while {action}ing blog : ", e)
        
        return render(request, "admin/blog/blog.html", {'blogs': blogs})
    
class BlogDeleteView(View):
    def post(self, request):
        try:
            blog = Blog.objects.get(id=request.POST.get("blog"))
            blog.active = False
            blog.save()
            messages.error(request, "blog deleted successfully.")
            return redirect('admin_blog_view')
        except Exception as e:
            blogs = blog.objects.filter(active=True)
            messages.error(request, "An error occurred while deleting blog : ", e)
            return render(request, "admin/blog/blog.html", {'blogs': blogs})

class AdminBlogView(View):
    def get(self, request, pk):
        """retrive blog if user is admin"""
        try:
            blog = Blog.objects.get(id=pk)
        except:
            messages.error(request, "blog is not available.")
        return render(request, "admin/blog/blog-description.html", {'blog': blog})

class UserBlogView(View):
    def get(self, request, pk):
        try:
            blog = Blog.objects.get(id=pk)
        except:
            messages.error(request, "blog is not available.")

        return render(request, "home/blog-details.html", {'blog': blog})
        