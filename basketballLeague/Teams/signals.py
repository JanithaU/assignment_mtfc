from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import LoginActivity

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    LoginActivity.objects.create(user=user, login_time=timezone.now())

@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    try:
        activity = LoginActivity.objects.filter(user=user, logout_time__isnull=True).latest('login_time')
        activity.logout_time = timezone.now()
        activity.save()
    except LoginActivity.DoesNotExist:
        pass  # No active login session found