from django import forms
from .models import Post

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

def min_length_5_validator(value):
    if len(value) < 5:
        raise forms.ValidationError('text은 5글자 이상 입력해주세요')


class PostForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea, validators=[min_length_5_validator])