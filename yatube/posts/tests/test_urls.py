from django.contrib.auth import get_user_model
from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Post, Group


User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.notauthor = User.objects.create_user(username='reader')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='Тестовое описание',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_notauthor = Client()
        self.authorized_client_notauthor.force_login(self.notauthor)

    def test_urls_correct_template_guest(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{PostURLTests.group.slug}/',
            'posts/profile.html': f'/profile/{PostURLTests.user}/',
            'posts/post_detail.html': '/posts/1/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_correct_template_author(self):
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_urls_correct_template_authorised(self):
        response = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_nonexistent_page(self):
        response = self.guest_client.get('/nonexisting/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_correct_redirect_guest(self):
        response = self.guest_client.get('/posts/1/edit/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/posts/1/edit/')
