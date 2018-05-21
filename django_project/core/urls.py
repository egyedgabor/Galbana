from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth.views import login

from .decorators import auth_check
from .views import Elastic, index

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', auth_check(login), {'template_name': 'login.html'},
        name='login'),
    path('/', include('django.contrib.auth.urls')),
    url(r'^home/', index.as_view()),
    url(r'^elastic/', Elastic.as_view()),
]
