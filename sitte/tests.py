from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Ad, Category
from django.core.files.uploadedfile import SimpleUploadedFile


class AdTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Электроника')

    def test_ad_creation(self):
        self.client.login(username='testuser', password='testpass')

        image = SimpleUploadedFile(
            name='test.jpg',
            content=b'smalljpeg',
            content_type='image/jpeg'
        )

        response = self.client.post(reverse('ad_create'), {
            'title': 'Test Ad',
            'description': 'Test description',
            'price': '1000.00',
            'category': self.category.id,
            'image': image,
        })

        print("Form errors:", response.context['form'].errors)  # ⬅️ Покажет, что именно не так

        self.assertEqual(response.status_code, 302)

