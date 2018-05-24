from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.views import login

from .decorators import auth_check
from .views import Sudo, index, Ssh, Postgres

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    url(r'^$', auth_check(login), {'template_name': 'login.html'},
        name='login'),
    url(r'^home/', index.as_view()),
    url(r'^sudo/', Sudo.as_view(), name='sudo'),
    url(r'^ssh/', Ssh.as_view(), name='ssh'),
    url(r'^postgres/', Postgres.as_view(), name='postgres'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
