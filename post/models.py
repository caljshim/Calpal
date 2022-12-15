from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save, post_delete
from django.urls import reverse

from notifications.models import Notifications

def user_directory_path(instance, filename):
    # this file will be uploaded to MEDIA_ROOT /user(id)/filename
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name='Picture', null=False)
    caption = models.TextField(max_length=1500, verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('postdetails', args=[str(self.id)])
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following

        notify = Notifications(sender=sender, user=following, notification_type=2)
        notify.save()

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()

post_save.connect(Stream.add_post, sender=Post)

post_save.connect(Follow.user_follow, sender=Follow)