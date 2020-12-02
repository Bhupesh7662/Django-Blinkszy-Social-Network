from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment

user = Post.author


class AddHotform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'hotimage', 'hotcaption')
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control col-md-6', 'value': '', 'id': 'user_id', 'type': 'hidden'}),
            'hotcaption': forms.Textarea(attrs={'class': 'form-control col-md-6'}),
        }


class UpdateHotform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('hotcaption',)
        widgets = {
            'hotcaption': forms.Textarea(attrs={'class': 'form-control col-md-6'}),
        }


class AddHotComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'value': ''}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UpdateHotCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control col-md-6'}),
        }
