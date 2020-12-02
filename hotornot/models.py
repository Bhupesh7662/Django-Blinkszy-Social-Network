from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db.models.signals import post_delete
from django.dispatch import receiver

# For compressing images while uploading
def compress(hotimage):
    im = Image.open(hotimage)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=30)
    new_image = File(im_io, name=hotimage.name)
    return new_image


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')
    hotcaption = models.TextField()
    hotimage = models.ImageField(
        upload_to='media/Hot_posts/%Y/%m/%d')
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='hot_post')

    def __str__(self):
        return self.author.username + " | " + str(self.created_date.date()) + " | " + str(self.created_date.time())

    def datepublished(self):
        return self.created_date.strftime('%B/ %d /%Y')

    def get_absolute_url(self):
        return reverse('Hot_or_not_home')

    def total_likes(self):
        return self.likes.count()

    # For compressing images while uploading
    def save(self, *args, **kwargs):
        new_image = compress(self.hotimage)
        self.hotimage = new_image
        super().save(*args, **kwargs)

# For Deleting the image after post is delete
@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.hotimage.delete(False)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post, self.name)

    # Redirecting to commented post after commenting
    def get_absolute_url(self):
        return reverse('hot_detail', args=[str(self.post.id)])