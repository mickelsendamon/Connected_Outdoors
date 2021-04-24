from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page),
    path('login', views.login),
    path('register', views.register_page),
    path('registration', views.register),
    path('logout', views.logout),
    path('adventures', views.adventures_page),
    path('new_adventure', views.new_adventure),
    path('create_adventure', views.create_adventure),
    path('my_adventures', views.my_adventures),
    path('join_adventure', views.join_adventure),
    path('leave_adventure', views.leave_adventure),
    path('adventure_details/<int:adv_id>', views.adventure_detail),
    path('cancel_adventure/<int:adv_id>', views.cancel_adventure),
]