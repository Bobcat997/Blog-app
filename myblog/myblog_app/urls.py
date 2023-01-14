from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('entries/', views.entries, name='entries'),
    path('entry/<int:entry_id>/', views.entry, name='entry'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
    path('entry/<int:entry_id>/add_comment', views.add_comment, name='add_comment'),
    path('entry/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
]