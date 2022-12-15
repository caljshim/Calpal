from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse

from notifications.models import Notifications

def ShowNotifications(request):
    user = request.user
    notifications = Notifications.objects.filter(user=user).order_by('-date')
    Notifications.objects.filter(user=user, is_seen=False).update(is_seen=True)

    template = loader.get_template('notifications.html')

    context = {
        'notifications': notifications,
    }

    return HttpResponse(template.render(context, request))

def DeleteNotifications(request, noti_id):
    user = request.user
    Notifications.objects.filter(id=noti_id, user=user).delete()
    return redirect('show-notifications')

def CountNotifications(request):
    count_notifications = 0
    if request.user.is_authenticated:
        count_notifications = Notifications.objects.filter(user=request.user, is_seen=False).count()

    return {'count_notifications': count_notifications}