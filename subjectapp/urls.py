from django.urls import path
from .views import (
    subject_signup_view,
    subject_login_view,
    subject_list_view,
    add_subject_view,
    edit_subject_view,
    delete_subject_view,
    subject_logout_view,
    subject_list_api,
    add_subject_api,
    subject_detail_api,
)

urlpatterns = [
    path('signup/', subject_signup_view, name='subject_signup'),
    path('login/', subject_login_view, name='subject_login'),
    path('subjects/', subject_list_view, name='subject_list'),
    path('add/', add_subject_view, name='add_subject'),
    path('edit/<int:pk>/', edit_subject_view, name='edit_subject'),
    path('delete/<int:pk>/', delete_subject_view, name='delete_subject'),
    path('logout/', subject_logout_view, name='logout'),

    path('api/subjects-list/',subject_list_api,name='subject_list_api'),
    path('api/add-subject/',add_subject_api,name='add_subject_api'),
    path('api/subjects/<int:pk>/',subject_detail_api,name='subject_detail_api'),
 
]
