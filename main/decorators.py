from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


# function for handling aunthentication
def allowed_users(allowed_roles=[], path="", message=""):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = None

            # excecuted if user has a group
            if request.user.groups.exists():
                groups = request.user.groups.all()

                for a in groups:

                    # executed when users group exist in allowed_roles, give this user access
                    if(a.name in allowed_roles):
                        return view_func(request, *args, **kwargs)

                    # exceuted when user group doesn't exist in allowed_roles, redirect them to a spesific path and send a message
                    else:
                        messages.success(request, message)
                        return redirect(path)

            # excecuted when user dont have a group, redirect them to a spesific path and send a message
            else:
                messages.success(request, message)
                return redirect(path)

        return wrapper_func
    return decorator
