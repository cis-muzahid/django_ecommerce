# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('admin/blog/', BlogView.as_view(), name='admin_blog_view'),
    path('admin/blog/delete', BlogDeleteView.as_view(), name='delete_blog_view'),
    path('user/blogs', UserBlogView.as_view(), name='user_blog_list'),
    path('user/blog/<int:pk>', UserBlogView.as_view(), name='user_blog'),
    path('admin/blog/<int:pk>', AdminBlogView.as_view(), name='admin_blog'),
    path('user/comment/', UserCommentView.as_view(), name='user_comment'),
    path('user/comment/delete/', DeleteCommentView.as_view(), name='delete_comment'),
]
