from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('login/', views.signin, name='signin'),
    path('registration/', views.registration, name='registration'),
    path('signout/', views.signout, name='signout'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

    path('top/', views.top, name='top'),
    path('new/', views.new, name='new'),

    path('user/<int:id>/', views.profile, name='user'),
    path('tag/<int:id>', views.tag, name='tag'),

    # path('post/<int:id>/preference/userpreference', views.preference, name='postpreference'),
]