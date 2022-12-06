from django import forms


class EmailPostForm(forms.Form):
    # Create post recommendation form
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea, required=False)
