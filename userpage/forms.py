from django import forms
from .models import Post, Comment


class UpdatePostform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption',)
        widgets = {
            'caption': forms.Textarea(attrs={'class': 'form-control col-md-6'}),
        }


class AddPostComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'Post_Comment')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-md-6', 'value': ''}),
            'Post_Comment': forms.Textarea(attrs={'class': 'form-control col-md-6'}),
        }
