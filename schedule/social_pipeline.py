from social_core.pipeline.partial import partial
from django.shortcuts import redirect
from schedule.models import User

@partial
def register(strategy, details, user=None, is_new=False, *args, **kwargs):
    if is_new:
        return redirect('new_user')
    else:
        return

def social_details(backend, details, response, *args, **kwargs):
    print(response['email'])
    try:
        user = User.objects.get(email=response['email'])
    except User.DoesNotExist:
        user = None
    if user:
        print(user.email)
        return 
    else:
        print(response)
        return redirect('new_user')

