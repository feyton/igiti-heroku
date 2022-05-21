from django.shortcuts import redirect


def staff_only(func_view):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return func_view(request, *args, **kwargs)
        return redirect('update-profile')

    return wrap


def nursery_manager(func_view):
    def wrap(request, *args, **kwargs):
        if request.user.userprofile.is_manager or request.user.is_staff:
            return func_view(request, *args, **kwargs)
        return redirect('notification')

    return wrap
