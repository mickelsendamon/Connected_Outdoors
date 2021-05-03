from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page),
    path('login', views.login),
    path('register', views.register_page),
    path('registration', views.registration),
    path('logout', views.logout),
    path('adventures', views.adventures_page),
    path('new_adventure', views.new_adventure),
    path('create_adventure', views.create_adventure),
    path('my_adventures', views.my_adventures),
    path('join_adventure/<int:adv_id>', views.join_adventure),
    path('leave_adventure/<int:adv_id>', views.leave_adventure),
    path('adventure_detail/<int:adv_id>', views.adventure_detail),
    path('cancel_adventure/<int:adv_id>', views.cancel_adventure),
    path('activity_form', views.create_activity),
    path('add_activity', views.add_activity),
    path('edit_adventure/<int:adv_id>', views.edit_adventure_page),
    path('edit_adventure/<int:adv_id>/update', views.edit_adventure),
    path('add_sg_equpiment', views.add_sg_equipment),
    path('filter_adventures', views.filter_adventures),
    path('filter_my_adventure', views.filter_my_adventures),
]
