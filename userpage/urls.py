from django.urls import path
from . import views
from .views import Search_User, UpdatePost, PostDetails, PostComment, DeletePost

urlpatterns = [
    path('', views.home, name="home"),
    path('post/', views.post, name="post"),
    path('update/post/<int:pk>', UpdatePost.as_view(), name="update_post"),
    path('delete_post/<int:id>', views.delete_post, name="delete_post"),
    path('<str:username>', views.user_profile, name="user_profile"),
    path('<int:post_id>/like_dislike_post/',
         views.like_dislike_post, name='like_dislike_post'),
    path("follow/<str:username>", views.follow, name="follow"),
    path('search/', Search_User.as_view(), name='search'),
    path('details/<int:pk>', PostDetails.as_view(), name='post_details'),
    path('delete/<int:pk>/post', DeletePost.as_view(), name='post_delete'),
    path('comment/<int:pk>/post', PostComment.as_view(), name='add_post_comment'),
    path('delete_post_comment/<int:id>', views.delete_post_comment, name="delete_post_comment"),
]
