from django.urls import path
from search.views import UserSearch

urlpatterns = [
    path('', UserSearch, name="search")
]