from django.contrib import admin
from post.models import Post, Follow, Stream
from . import models

admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
