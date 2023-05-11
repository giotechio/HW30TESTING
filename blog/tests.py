from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

# Create your tests here.

class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email='test@email.com',
            password = 'abracadabra'
        )

        self.post = Post.objects.create(
            title = 'Test title',
            body = 'Test content',
            author = self.user
        )

    def test_string_representation(self):
        post = Post(title='Test title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'Test title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}','Test content' )

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test content')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test title')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'),{
            'title':'Test title',
            'body':'Test text',
            'author':self.user, })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test title')
        self.assertContains(response, 'Test text')

    def test_post_update_view(self):
        response=self.client.post(reverse('post_edit', args='1'),{'title':'Updated title', 'body':'Updated body', })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.get(
            reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)

