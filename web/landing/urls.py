from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('signup/', views.sign_up, name="signup"),
    path('signup/confirm/', views.sign_up_confirm, name="signup_confirm"),
    path('login/', views.login, name='login'),
    path('login/confirm/', views.login_confirm, name="login_confirm"),
    path('logout/', views.logout_view, name='logout'),

    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment'),

    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

    path('tag/<int:id>', views.tag, name='tag'),
]