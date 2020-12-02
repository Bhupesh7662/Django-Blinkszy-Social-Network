from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from hotornot.models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import AddHotform, UpdateHotform, AddHotComment, UpdateHotCommentForm
# import json
# from django.conf import settings


class Home(ListView):
    model = Post
    template_name = 'hotornot/hotornot.html'
    ordering = ['-created_date']


class HotDetails(DetailView):
    model = Post
    template_name = 'hotornot/hot_details.html'

    # Hot Counting (likes)
    def get_context_data(self, *args, **kwargs):
        context = super(HotDetails, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class AddHotPost(CreateView):
    model = Post
    form_class = AddHotform
    template_name = 'hotornot/hot_add.html'


class UpdateHotPost(UpdateView):
    model = Post
    form_class = UpdateHotform
    template_name = 'hotornot/update_hot.html'


def delete_hot_post(request, id):
    post_ = Post.objects.get(id=id)
    post_.delete()
    return redirect('home')

# Like hot Post
def LikehotPost(request, pk):
    post_id = request.POST.get('post_id')
    hotPost = get_object_or_404(Post, id=post_id)
    liked = False
    if hotPost.likes.filter(id=request.user.id).exists():
        hotPost.likes.remove(request.user)
        liked = False
    else:
        hotPost.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('hot_detail', args=[str(pk)]))


# Comments
class AddHotComment(CreateView):
    model = Comment
    form_class = AddHotComment
    template_name = 'hotornot/add_comments.html'
    ordering = ['-created_date']

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


def delete_hot_comment(request, id):
    comment_ = Comment.objects.get(id=id)
    comment_.delete()
    return HttpResponse('success')


# Hot Post to profile section
def user_hot_profile(request, username):
    user = User.objects.filter(username=author)
    if user:
        user = user[0]
        # profile = Profile.objects.get(user=user)
        post = getPost(user)
        context = {
            'user_data': user,
            'post_hot': post,
        }
    else:
        return HttpResponse('No Such User :( ')
    return render(request, 'userpage/user_profile.html', context)


def getHotPost(user):
    post_obj = Post.objects.filter(user=user)
    imgList = [post_obj[i:i+3] for i in range(0, len(post_obj), 3)]
    return imgList
