from django.urls import path, include
from authy.views import UserProfile, Signup, EditProfile, Login, Logout

from django.contrib.auth import views as authViews 



urlpatterns = [
   	path('signup/', Signup, name='signup'),
   	path('login/', Login, name='login'),
    path('profile/edit', EditProfile, name='edit-profile'),
   	path('logout/', Logout, name='logout'),
]