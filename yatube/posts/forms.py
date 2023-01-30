from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Введите текст',
            'group': 'Выберите группу'
        }
        help_texts = {
            'text': 'Текст поста, можно написать что-нибудь хорошее:))',
            'group': 'Группы сети Yatube'
        }

    def clean_text(self):
        data = self.cleaned_data['text']

        if '' not in data.lower():
            raise forms.ValidationError('необходимо заполнить поле')
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
