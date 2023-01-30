from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import (PasswordChangeView,
                                       PasswordChangeDoneView)
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import (PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.urls import path
from . import views

app_name = 'users'
PCV = PasswordChangeView
PCDV = PasswordChangeDoneView
PRV = PasswordResetView
PRDV = PasswordResetDoneView
PRCV = PasswordResetConfirmView
PRCLV = PasswordResetCompleteView
# строка получилась длинной, заменил на константу

urlpatterns = [
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path(
        'signup/',
        views.SignUp.as_view(template_name='users/signup.html'),
        name='signup'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'password_change/',
        PCV.as_view(template_name=('users/password_change_form.html')),
        name='password_change_form'
    ),
    path(
        'password_change/done/',
        PCDV.as_view(template_name='users/password_change_done.html'),
        name='password_change_done'
    ),
    path(
        'password_reset/',
        PRV.as_view(template_name='users/password_reset_form.html'),
        name='password_reset_form'
    ),
    path(
        'password_reset/done/',
        PRDV.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PRCV.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        PRCLV.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]
