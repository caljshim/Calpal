from typing import get_origin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from comment.forms import CommentForm

from post.models import Post, Stream
from post.forms import NewPostForm
from comment.models import Comment
from django.urls import reverse

@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)

    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    template = loader.get_template('index.html')

    context = {
        'post_items': post_items,
    }
    return HttpResponse(template.render(context, request))

@login_required
def postdetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    template = loader.get_template('post_detail.html')

    comments = Comment.objects.filter(post=post).order_by('date')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
    else:
        form = CommentForm()
        
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return HttpResponse(template.render(context, request))


@login_required
def newpost(request):
    user = request.user.id
    tags_objs = []

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')

            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.save()
            return redirect('index')

    else:
        form = NewPostForm

    context = {
        'form' : form,
    }

    return render(request, 'newpost.html', context)

