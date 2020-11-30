from django.shortcuts import redirect


def anonymous_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return view_func(request, *args, **kwargs)

        else:
            return redirect('activity:home')

    return wrapper_func
