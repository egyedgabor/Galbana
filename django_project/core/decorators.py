# Django core and 3rd party imports
from django.http import HttpResponseRedirect
from django.conf import settings


def auth_check(view_func):
    """ Check the user. If (s)he is authenticated redirect hem/him to the
        LOGIN_REDIRECT_URL else show the login page """
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


def admin_check(view_func):
    """ Check the user. If (s)he is an admin than show her/him the page
        else redirect her/him to the login page """
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_anonymous and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        url = settings.LOGIN_URL + '?next=' + request.path_info
        return HttpResponseRedirect(url)
    return _wrapped_view_func
