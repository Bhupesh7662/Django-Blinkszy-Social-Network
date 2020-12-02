from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from userpage.models import Post, Profile, Like, Following, Comment
from django.conf import settings
import json
from hotornot.views import getHotPost
# from django.core.paginator import Paginator
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from .forms import UpdatePostform, AddPostComment


def home(request):
    user = Following.objects.get(user=request.user)
    followed_users = user.followed.all()

    post_data = Post.objects.filter(user__in=followed_users).order_by(
        '-pk') | Post.objects.filter(user=request.user).order_by('-pk')

    liked_ = [i for i in post_data if Like.objects.filter(
        post=i, user=request.user)]

    context = {
        'post': post_data,
        'liked_post': liked_,
    }

    return render(request, 'userpage/home.html', context)


def post(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        user = request.user
        postimage = request.FILES.get('postimage')
        if postimage:
            post_data = Post(caption=caption, user=request.user,
                             postimage=postimage)
        else:
            post_data = Post(caption=caption, user=request.user)

        post_data.save()
        messages.success(request, ': Your post uploaded successfully!')
        return redirect('home')
    else:
        messages.error(request, ': Something went wrong :( ')
        return redirect('home')


class UpdatePost(UpdateView):
    model = Post
    form_class = UpdatePostform
    template_name = 'userpage/update_post.html'


def delete_post(request, id):
    post_ = Post.objects.get(id=id)
    post_.delete()
    return redirect('home')


def user_profile(request, username):
    user = User.objects.filter(username=username)
    if user:
        user = user[0]
        profile = Profile.objects.get(user=user)
        post = getPost(user)
        user_img = profile.userImage
        bio = profile.bio
        connection = profile.connection
        follower = profile.follower
        following = profile.following
        is_following = Following.objects.filter(
            user=request.user, followed=user)
        # To create following object
        following_obj = Following.objects.get(user=user)
        # Counting followers
        follower, following = following_obj.follower.count(), following_obj.followed.count()

        context = {
            'user_data': user,
            'bio': bio,
            'user_img': user_img,
            'connection': connection,
            'follower': follower,
            'following': following,
            'posts': post,
            'hot': getHotPost,
            'follow_connection': is_following
        }
    else:
        return HttpResponse('No Such User :( ')
    return render(request, 'userpage/user_profile.html', context)


def getPost(user):
    post_obj = Post.objects.filter(user=user)
    imgList = [post_obj[i:i+3] for i in range(0, len(post_obj), 3)]
    return imgList


def like_dislike_post(request, post_id):
    post_id = request.GET.get('post_id', )
    print(post_id)
    post = Post.objects.get(pk=post_id)
    user = request.user
    like = Like.objects.filter(post=post, user=user)

    liked = False

    if like:
        Like.dislike(post, user)
    else:
        liked = True
        Like.like(post, user)

    resp = {
        'liked': liked
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")


def follow(request, username):
    main_user = request.user.id
    to_follow = User.objects.get(username=username)

    # checking if already following
    following = Following.objects.filter(user=main_user, followed=to_follow)
    is_following = True if following else False

    if is_following:
        Following.unfollow(main_user, to_follow)
        is_following = False
    else:
        Following.follow(main_user, to_follow)
        is_following = True

    resp = {
        "following": is_following,
    }

    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")


class Search_User(ListView):
    model = User
    template_name = "userpage/search.html"

    def get_queryset(self):
        username = self.request.GET.get("username", "")
        queryset = User.objects.filter(username__icontains=username)
        return queryset


class PostDetails(DetailView):
    model = Post
    template_name = 'userpage/post_details.html'
    ordering = ['-created_date']


class DeletePost(DeleteView):
    model = Post
    template_name = 'userpage/delete_post.html'
    success_url = reverse_lazy('home')


# Comments
class PostComment(CreateView):
    model = Comment
    form_class = AddPostComment
    template_name = 'userpage/post_comments.html'
    ordering = ['-created_date']

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


def delete_post_comment(request, id):
    comment_ = Comment.objects.get(id=id)
    comment_.delete()
    return HttpResponse('success')
