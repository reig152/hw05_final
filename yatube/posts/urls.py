from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path(
        'group/<str:slug>/',
        views.GroupPostsView.as_view(),
        name='group_list'
    ),
    path(
        'profile/<str:username>/',
        views.UserPostsView.as_view(),
        name='profile'
    ),
    path(
        'posts/<int:post_id>/',
        views.PostDetail.as_view(),
        name='post_detail'
    ),
    path('create/', views.PostCreate.as_view(), name='post_create'),
    path('posts/<int:post_id>/edit/',
         views.PostEdit.as_view(),
         name='post_edit'),
    path(
        'posts/<int:post_id>/comment/',
        views.PostDetail.as_view(),
        name='add_comment'
    ),
    path('follow/', views.FollowIndex.as_view(), name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),
]
