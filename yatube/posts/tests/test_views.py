import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django import forms
from posts.models import Post, Group


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='Тестовое описание',
        )
        cls.second_group = Group.objects.create(
            title='Тестовая группа 2',
            slug='test_group_2',
            description='Тестовое описание 2',
        )
        cls.image = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        small_gif = SimpleUploadedFile(
            name='small.gif',
            content=cls.image,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый текст',
            image=small_gif,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_index_page_show_correct_context(self):

        """Шаблон index сформирован с правильным контекстом."""

        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_text_0, 'Тестовый текст')
        self.assertEqual(post_group_0, 'Тестовая группа')

    def test_group_list_show_correct_context(self):

        """Шаблон group_list сформирован с правильным контекстом."""

        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        post_group_slug_0 = first_object.group.slug
        post_group_description_0 = first_object.group.description
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_text_0, 'Тестовый текст')
        self.assertEqual(post_group_0, 'Тестовая группа')
        self.assertEqual(post_group_slug_0, 'test_group')
        self.assertEqual(post_group_description_0, 'Тестовое описание')

    def test_profile_show_correct_context(self):

        """Шаблон profile сформирован с правильным контекстом."""

        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        post_group_slug_0 = first_object.group.slug
        post_group_description_0 = first_object.group.description
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_text_0, 'Тестовый текст')
        self.assertEqual(post_group_0, 'Тестовая группа')
        self.assertEqual(post_group_slug_0, 'test_group')
        self.assertEqual(post_group_description_0, 'Тестовое описание')

    def test_post_detail_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        first_object = response.context['post']
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image.name
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_text_0, 'Тестовый текст')
        self.assertEqual(post_group_0, 'Тестовая группа')
        self.assertEqual(post_image_0, 'posts/small.gif')

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs=(
                {'slug': self.group.slug})): 'posts/group_list.html',
            reverse('posts:profile', kwargs=(
                {'username': self.user})): 'posts/profile.html',
            reverse('posts:post_detail', kwargs=(
                {'post_id': self.post.id})): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs=(
                {'post_id': self.post.id})): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        first_object = response.context['post']
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_text_0, 'Тестовый текст')
        self.assertEqual(post_group_0, 'Тестовая группа')

    def test_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_added_on_correct_page(self):
        reverse_page_templates = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug
            }),
            reverse('posts:profile', kwargs={
                'username': self.user
            })
        ]
        for page_templates in reverse_page_templates:
            with self.subTest(page_templates=page_templates):
                response = self.authorized_client.get(page_templates)
                first_object = response.context['page_obj'][0]
                post_text_0 = first_object.text
                self.assertEqual(post_text_0, self.post.text)

    def test_correct_group(self):
        response_first_group_check = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test_group'}))
        response_second_group_check = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test_group_2'}))
        first_group_page = response_first_group_check.context['page_obj']
        second_group_page = response_second_group_check.context['page_obj']
        self.assertIn(self.post, first_group_page.paginator.object_list)
        self.assertNotIn(self.post, second_group_page.paginator.object_list)

    def test_comment_is_on_page(self):
        self.authorized_client.post(reverse('posts:add_comment',
                                    kwargs={'post_id': self.post.id}),
                                    {'text': "Тестовый комментарий"},
                                    follow=True)
        response = self.authorized_client.get(f'/posts/{self.post.id}/')
        self.assertContains(response, 'Тестовый комментарий')


class PaginatorViewsTest(TestCase):
    ALL_POSTS = 13
    FIRST_PAGE = 10
    SECOND_PAGE = 3

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='Тестовое описание',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        context: list = []
        for x in range(self.ALL_POSTS):
            context.append(
                Post(
                    text=f'Тестовый текст для {x} поста',
                    group=self.group,
                    author=self.user
                )
            )
        Post.objects.bulk_create(context)

    def test_all_pages_contains_needed_records(self):
        reverse_name_posts = {
            reverse('posts:index'): self.FIRST_PAGE,
            reverse('posts:index') + '?page=2': self.SECOND_PAGE,
            reverse('posts:group_list', kwargs={
                'slug': 'test_group'
            }) + '?page=2': self.SECOND_PAGE,
            reverse('posts:group_list', kwargs={
                'slug': 'test_group'
            }): self.FIRST_PAGE,
            reverse('posts:profile', kwargs={
                'username': 'auth'
            }): self.FIRST_PAGE,
            reverse('posts:profile', kwargs={
                'username': 'auth'
            }) + '?page=2': self.SECOND_PAGE,
        }
        for reverse_name, posts in reverse_name_posts.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), posts)
