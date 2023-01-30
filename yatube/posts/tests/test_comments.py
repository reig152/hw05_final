from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Post, Group
from django.urls import reverse
from django import forms

User = get_user_model()


class CommentTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый текст',
        )

        cls.form_fields = {
            'text': forms.fields.CharField,
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_comments_alright(self):
        """Форма создания комментария работает исправно"""
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={
                'post_id': self.post.pk
            }
        ))
        for value, expected in self.form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)
