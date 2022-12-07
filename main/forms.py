from django import forms
from main.models import Comment


class EmailPostForm(forms.Form):
    # Create post recommendation form
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    # Create comment model form
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
