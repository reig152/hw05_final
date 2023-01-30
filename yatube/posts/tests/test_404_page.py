from django.test import Client, TestCase


class TestErrorPage(TestCase):
    @classmethod
    def setUp(self):
        self.guest_client = Client()

    def test_404_correct_template(self):
        """Страница ошибки использует правильный шаблон"""
        response = self.guest_client.get('/unexisting_pages/')
        self.assertTemplateUsed(response, 'core/404.html')
