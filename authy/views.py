from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, EditProfileForm
from django.contrib.auth.models import User
from post.models import Post, Follow, Stream
from django.db import transaction

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout

from authy.models import Profile
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator
from django.urls import resolve, reverse

# Create your views here.
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name

	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')

	#Profile info
	post_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	#Follow status
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	#Pagination
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
		'posts': posts_paginator,
		'profile': profile,
		'url_name': url_name,
		'posts_count': post_count,
		'following_count': following_count,
		'followers_count': followers_count,
		'follow_status': follow_status,
	}

	return HttpResponse(template.render(context, request))


def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('login')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'signup.html', context)

def Login(request):
	error = False
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			error = True

	context = {
		'error': error
	}
	return render(request, 'login.html', context)

def Logout(request):
	logout(request)
	return redirect('login')
	

@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	username = request.user.username

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return redirect(reverse('profile', args=[username]))
	else:
		form = EditProfileForm()

	context = {
		'form':form,
	}

	return render(request, 'editprofile.html', context)

@login_required
def FollowUser(request, username, option):
	user = request.user
	following = get_object_or_404(User, username=username)

	try:
		f, created = Follow.objects.get_or_create(follower=request.user, following=following)

		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following, user=user).all().delete()
		else:
			posts = Post.objects.all().filter(user=following)[:10]

			with transaction.atomic():
				for post in posts:
					stream = Stream(post=post, user=user, date=post.posted, following=following)
					stream.save()
		return HttpResponseRedirect((reverse('profile', args=[username])))
	except User.DoesNotExist:
		return HttpResponseRedirect((reverse('profile', args=[username])))
