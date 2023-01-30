from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Post, Group
from django.core.cache import cache
from django.urls import reverse


User = get_user_model()


class IndexPageCacheTest(TestCase):
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

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_index_cache(self):
        """Проверка кэша главной страницы"""
        cache.clear()
        f_response = self.authorized_client.get(reverse('posts:index'))
        f_post = Post.objects.get(id=1)
        f_post.delete()
        s_response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(f_response.content, s_response.content)
        cache.clear()
        t_response = self.authorized_client.get(reverse('posts:index'))
        self.assertNotEqual(f_response.content, t_response.content)
