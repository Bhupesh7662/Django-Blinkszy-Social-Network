from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse, reverse_lazy
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db.models.signals import post_delete
from django.dispatch import receiver


# For compressing images while uploading
def compress(postimage):
    im = Image.open(postimage)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=30)
    new_image = File(im_io, name=postimage.name)
    return new_image


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField()
    postimage = models.ImageField(upload_to='media/posts/%Y/%m/%d', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " | " + str(self.created_date.date()) + " | " + str(self.created_date.time())

    def datepublished(self):
        return self.created_date.strftime('%B/ %d /%Y')

    def get_absolute_url(self):
        return reverse('home')

    # For compressing images while uploading
    def save(self, *args, **kwargs):
        new_image = compress(self.postimage)
        self.postimage = new_image
        super().save(*args, **kwargs)

# For Deleting the image after post is delete
@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.postimage.delete(False)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userImage = models.ImageField(
        upload_to="media/profiles/%Y/%m/%d'", default="user.png")
    bio = models.CharField(max_length=100, blank=True)
    connection = models.CharField(max_length=100, blank=True)
    follower = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Like(models.Model):
    user = models.ManyToManyField(User, related_name="likingUser")
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    # For liking post
    @classmethod
    def like(cls, post, liking_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.add(liking_user)

    # For disliking post
    @classmethod
    def dislike(cls, post, disliking_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.remove(disliking_user)

    def __str__(self):
        return str(self.post) + ' | ' + str(self.post.id)


class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followed = models.ManyToManyField(User, related_name="followed")
    follower = models.ManyToManyField(User, related_name="follower")

    @classmethod
    def follow(cls, user, another_account):
        obj = cls.objects.get(user=user)
        obj.followed.add(another_account)

    @classmethod
    def unfollow(cls, user, another_account):
        obj = cls.objects.get(user=user)
        obj.followed.remove(another_account)

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='post_comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    Post_Comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    # comment_reply = models.ForeignKey('self', null=True, related_name='comment_replies', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return '%s - %s' % (self.post, self.name)

    # Redirecting to commented post after commenting
    def get_absolute_url(self):
        return reverse('post_details', args=[str(self.post.id)])
