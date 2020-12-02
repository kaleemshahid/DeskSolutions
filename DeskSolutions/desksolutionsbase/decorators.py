from django.http import HttpResponse
from django.shortcuts import redirect
from account.models import Organization
from django.contrib import messages


def organization_absent(view_func):
    def wrapper_func(request, *args, **kwargs):
        session_name = request.session.get('organization')
        print(session_name)
        if session_name is not None:
            print('in decorator')
            return view_func(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.INFO, 'Hello world.')
            return redirect('signup:home')

    return wrapper_func
