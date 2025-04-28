from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('dashboard',views.dashboard),
    path('create_project',views.create_project),
    path('project_info/<int:project_id>',views.project_info),
    path('edit_project/<int:project_id>',views.edit_project),
    path('delete_project',views.delete_project),
    path('join_project',views.join_project),
    path('leave_project',views.leave_project)
]