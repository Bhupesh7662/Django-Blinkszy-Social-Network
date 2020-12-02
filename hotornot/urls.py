from django.urls import path, include
from . import views
from .views import Home, AddHotPost, UpdateHotPost, HotDetails, AddHotComment

urlpatterns = [
    path('', Home.as_view(), name='Hot_or_not_home'),
    path('add_hot/', AddHotPost.as_view(), name="add_hot"),
    path('update_hot/<int:pk>', UpdateHotPost.as_view(), name="update_hot"),
    path('delete_hot_post/<int:id>', views.delete_hot_post, name="delete_hot_post"),
    path('detail/<int:pk>', HotDetails.as_view(), name="hot_detail"),
    path('like/<int:pk>', views.LikehotPost, name="like_hot"),
    path('hot/<int:pk>/comment', AddHotComment.as_view(), name="add_comment"),
    path('delete_hot_comment/<int:id>', views.delete_hot_comment, name="delete_hot_comment")
]