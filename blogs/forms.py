from django import forms

from members.models import Registration
from .models import Post, Category


class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['author'].queryset = Registration.objects.filter(
            user=self.request.user
        )

    class Meta:
        model = Post
        exclude = ('slug', 'timestamp', 'comments', 'date')
