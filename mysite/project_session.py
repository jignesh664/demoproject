
from django.shortcuts import reverse,redirect
from django.http import HttpResponseRedirect,HttpResponse

# decorators for session check

def check_session(func):
    def awrap(request, *args, **kwargs):
        if 'email' not in request.session:
            return HttpResponseRedirect(reverse('admin_login'))
        else:
            return func(request, *args, **kwargs)
    return awrap