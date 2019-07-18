from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.account_home, name='accounts-home'),
    path('account/<str:username>', views.view_account, name='accounts-account'),
    path('edit_account/<str:username>', views.edit_account, name='accounts-edit_account'),
    path('account/edit_avatar/<str:username>', views.edit_avatar, name='accounts-edit_avatar'),
    path('account/change_password/<str:username>', views.change_password, name='accounts-change_password'),
    path('sign_in/', views.sign_in, name='accounts-sign_in'),
    path('sign_up/', views.sign_up, name='accounts-sign_up'),
    path('sign_out/', views.sign_out, name='accounts-sign_out'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)