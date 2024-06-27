from django.shortcuts import render, redirect
from .models import Blog, Comment
from django.views import View
from django.contrib import messages
from .forms import BlogForm, CommentForm
from django.urls import reverse

# Create your views here.
class BlogView(View):
    def get(self, request):
        """ Admin blogs view """
        blogs = Blog.objects.filter(active=True)
        return render(request, "admin/blog/blog.html", {'blogs': blogs })

    def post(self, request):
        """ Admin create and update view for blog """
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
        """ Blog Delete View """
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
            comments = Comment.objects.filter(active=True, blog=blog, parent_comment=None)
        except:
            messages.error(request, "blog is not available.")
        return render(request, "admin/blog/blog-description.html", {'blog': blog, 'comments': comments})

class UserBlogView(View):
    def get(self, request, pk=None):
        """ User blog and blogs View """
        try:
            if pk == None:
                blogs = Blog.objects.filter(active=True)
                return render(request, "home/blogs.html", {'blogs': blogs})
            else:
                blog = Blog.objects.get(id=pk)
                comments = Comment.objects.filter(active=True, blog=blog, parent_comment=None)
                return render(request, "home/blog-details.html", {'blog': blog, 'comments': comments})
        except:
            messages.error(request, "blog is not available.")
            return render(request, "home/blog-details.html", {'blog': blog})

class UserCommentView(View):
    def post(self, request):
        """ Create and Update view for comment """
        if request.POST.get("pk"):
            action = "updat"
            comment = Comment.objects.get(id=request.POST.get("pk"))
            form = CommentForm(request.POST, request.FILES, instance=comment)
        else:
            action = "add"
            form = CommentForm(request.POST, request.FILES)

        blog = Blog.objects.get(id=request.POST.get("blog"))
        try:
            if form.is_valid():
                form.save()
                messages.success(request, f" Comment {action}ed successfully.")
                return redirect('user_blog', pk=blog.id)
            else:
                messages.error(request, f"An error occurred while {action}ing Comment : ", form.errors)
        except Exception as e:
            messages.error(request, f"An error occurred while {action}ing Comment : ", e)
        return render(request, "home/blog-details.html", {'blog': blog})

class DeleteCommentView(View):
    def post(self, request):
        """ Delete comment view """
        blog = Blog.objects.get(id=request.POST.get("blog"))
        try:
            comment = Comment.objects.get(id=request.POST.get("comment"))
            comment.active = False
            comment.save()
            messages.error(request, "comment deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while deleting Comment : ", e)
        return redirect('user_blog', pk=blog.id)
