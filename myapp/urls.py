
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('state/',views.state,name='state'),
    path('add_state/',views.add_state,name='add_state'),
    path('edit_state/<str:state_id>',views.edit_state,name='edit_state'),
    path('edit_state/',views.edit_state,name='edit_state'),
    path('delete_state/<str:st_id>',views.delete_state,name='delete_state'),
    path('city/',views.city,name='city'),
    path('add_city/',views.add_city,name='add_city'),
    path('edit_city/',views.edit_city,name='edit_city'),
    path('edit_city/<str:city_id>',views.edit_city,name='edit_city'),
    path('delete_city/<str:ct_id>',views.delete_city,name='delete_city'),
    path('area/',views.area,name='area'),
    path('add_area/',views.add_area,name='add_area'),
    path('edit_area/',views.edit_area,name='edit_area'),
    path('edit_area/<str:area_id>',views.edit_area,name='edit_area'),
    path('delete_area/<str:at_id>',views.delete_area,name='delete_area'),
    path('user/',views.user,name='user'),
    path('add_user/',views.add_user,name='add_user'),
    path('edit_user/',views.edit_user,name='edit_user'),
    path('edit_user/<str:user_id>',views.edit_user,name='edit_user'),
    path('delete_user/<str:ur_id>',views.delete_user,name='delete_user'),
    path('getcity/',views.getcity,name='getcity'),
    path('getarea/',views.getarea,name='getarea'),
    path('change_status_city/',views.change_status_city,name='change_status_city'),
    path('change_status_state/',views.change_status_state,name='change_status_state'),
    path('change_status_area/',views.change_status_area,name='change_status_area'),
    path('change_status_user/',views.change_status_user,name='change_status_user'),
    path('',views.admin_login,name='admin_login'),
    path('logout/',views.logout,name='logout'),
    path('forgot_pass/',views.forgot_pass,name='forgot_pass'),
    ]






