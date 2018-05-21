from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredMixin(LoginRequiredMixin):
    login_url = '/'
    redirect_field_name = 'redirect_to'
