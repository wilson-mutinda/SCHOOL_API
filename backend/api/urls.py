from django.urls import path
from . import views

urlpatterns = [
    path('create_custom_user/', views.list_create_custom_user_view, name='custom_user'),
    path('custom_user_info/<int:pk>/', views.retreive_update_delete_custom_user_view, name='custom_user_info'),
    path('user_login/', views.user_login_view, name='user_login'),

    path('create_role/', views.list_create_role_view, name='roles'),
    path('role_info/<int:pk>/', views.retreive_update_delete_role_view, name='role_info'),
    path('create_teacher/', views.create_teacher_view, name='teacher'),
    path('create_parent/', views.create_parent_view, name='parent'),
    path('create_student/', views.create_student_view, name='student'),
]
