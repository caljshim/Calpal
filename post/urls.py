from post.views import index, newpost, postdetails
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('newpost/', newpost, name='newpost'),
    path('<uuid:post_id>', postdetails, name='postdetails'),
]