from django import forms

from HairSaloon.common.models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'content']
