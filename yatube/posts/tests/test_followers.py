from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Post, Group
from django.urls import reverse

User = get_user_model()


class IndexPageCacheTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.follower = User.objects.create_user(username='follower')
        cls.following = User.objects.create_user(username='following')
        cls.another = User.objects.create_user(username='anotherUser')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='Тестовое описание',
        )

        cls.post_to_follow = Post.objects.create(
            author=cls.following,
            group=cls.group,
            text='Тестовый текст для подписоты',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_follower = Client()
        self.authorized_follower.force_login(self.follower)
        self.authorized_another = Client()
        self.authorized_another.force_login(self.another)

    def test_new_article_for_follower(self):
        """
        Новая запись пользователя появляется в ленте тех, кто
        на него подписан и не появляется в ленте тех, кто не подписан.
        """
        # подписываемся на автора
        self.authorized_follower.post(
            reverse('posts:profile_follow', kwargs={
                'username': 'following'}))

        # переходим на страницу с подписками
        follower_response = self.authorized_follower.get(
            reverse('posts:follow_index'))

        # должен быть 1 пост, так как подписался на автора с 1 постом
        self.assertEqual(len(follower_response.context['page_obj']), 1)

        # должно быть 0 постов
        another_response = self.authorized_another.get(
            reverse('posts:follow_index'))
        self.assertEqual(len(another_response.context['page_obj']), 0)

    def test_follow_and_unfollow(self):
        """Авторизованный пользователь может подписываться
           на других пользователей и удалять их из подписок"""

        # подписываемся на автора
        self.authorized_follower.post(
            reverse('posts:profile_follow', kwargs={
                'username': 'following'}))

        # переходим на страницу с подписками
        follower_response = self.authorized_follower.get(
            reverse('posts:follow_index'))

        # должен быть 1 пост, так как подписался на автора с 1 постом
        self.assertEqual(len(follower_response.context['page_obj']), 1)

        # отписываемся от автора
        self.authorized_follower.post(
            reverse('posts:profile_unfollow', kwargs={
                'username': 'following'}))

        # переходим на страницу с подписками
        follower_response = self.authorized_follower.get(
            reverse('posts:follow_index'))

        # отписались, теперь 0 постов
        self.assertEqual(len(follower_response.context['page_obj']), 0)
