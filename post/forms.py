from django import forms
from post.models import Post

class NewPostForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.Textarea(), required=True)

    class Meta:
        model = Post
        fields = ('picture', 'caption')

