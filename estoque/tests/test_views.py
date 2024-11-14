import json
from django.http import JsonResponse
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator

class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@test.com', password='password')

    def test_login_view(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_redirect_authenticated_user(self):
        session = self.client.login(username='user', password='password')
        resp = self.client.get('')
        self.assertRedirects(resp, '/dashboard/')

    def test_redirect_post_authentication(self):
        resp = self.client.post('', {'username': 'user', 'password': 'password'})
        self.assertRedirects(resp, '/dashboard/')

    def test_not_authenticated_user(self):
        resp = self.client.get('')
        self.assertTemplateUsed(resp, template_name='login.html')


class PasswordResetConfirmTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(id=1, username='user', email='user@test.com', password='password')

    def test_password_reset_confirm(self):
        uidb64 = 'MQ=='
        token = default_token_generator.make_token(self.user)
        print(token)
        resp = self.client.get(f'/reset/{uidb64}/{token}/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(type(resp.context['form']), SetPasswordForm)

    def test_password_reset_confirm_user_does_not_exists(self):
        resp = self.client.get('/reset/test/123/')
        self.assertEqual(type(resp.context['form']), None.__class__)

    def test_password_reset_confirm_post(self):
        token = default_token_generator.make_token(self.user)
        resp = self.client.post(f'/reset/MQ==/{token}/', data={'new_password1': 'testingpassw123',
                                                          'new_password2': 'testingpassw123'})
        self.assertRedirects(resp, '/dashboard/')


class DashboardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(id=1, first_name= 'first_name', last_name='last_name', username='user', email='user@test.com', password='password')

    def test_dashboard(self):
        session = self.client.login(username='user', password='password')
        resp = self.client.get('/dashboard/')
        self.assertTemplateUsed('dashboard.html')
        self.assertEqual(resp.status_code, 200)


class GetUserDataTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(id=1, first_name= 'first_name', last_name='last_name', username='user', email='user@test.com', password='password')

    def test_get_user_data(self):
        session = self.client.login(username='user', password='password')
        resp = self.client.get(f'/get_user_data/{self.user.id}/')
        self.assertEqual(resp.status_code, 200)

    def test_get_user_data_when_user_not_exists(self):
        session = self.client.login(username='user', password='password')
        resp = self.client.get(f'/get_user_data/9/')
        self.assertRaises(User.DoesNotExist)


class SaveUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(id=10, first_name= 'first_name', last_name='last_name', username='user', email='user@test.com', password='password')

    def test_save_user(self):
        session = self.client.login(username='user', password='password')
        resp = self.client.post('/save_user/', {'user_id': self.user.id, 'first_name': 'test', 'last_name': 'test',
                                                'email': 'user2@test.com', 'username': 'user'})
        self.assertEqual(json.loads(resp.content), {'success': True, 'user_id': self.user.id})

    def test_save_user_creation(self):
        session = self.client.login(username='user', password='password')
        resp = self.client.post('/save_user/', {'first_name': 'test', 'last_name': 'test',
                                                'email': 'user2@test.com', 'password1': 'SecurePass!2024',
                                                'password2': 'SecurePass!2024', 'username': 'newuser'})
        self.assertTrue('success' in json.loads(resp.content) and json.loads(resp.content)['success'] == True)
    
    def test_save_user_not_valid_form(self):
        session = self.client.login(username='user', password='password')
        resp = self.client.post('/save_user/', {'user_id': self.user.id, 'first_name': 'test', 'last_name': 'test',
                                                'email': 'user2@@testxcom', 'username': 'user'})
        self.assertNotEqual(json.loads(resp.content), {'success': True, 'user_id': self.user.id})

    def test_save_user_creation_not_valid_form(self):
        session = self.client.login(username='user', password='password')
        resp = self.client.post('/save_user/', {'first_name': 'test', 'last_name': 'test',
                                                'email': 'user2@@testxcom', 'password1': 'password1'})
        self.assertTrue('success' in json.loads(resp.content) and json.loads(resp.content)['success'] == False)


class ExportUsersTest(TestCase):
    def setUp(self):
       self.user = User.objects.create_user(id=1, username='user', email='user@test.com', password='password')
    
    def test_export_user_login_required(self):
        response = self.client.get('/export_users/')
        self.assertEqual(response.status_code, 302)

    def test_export_user(self):
        session = self.client.login(username='user', password='password')
        response = self.client.get('/export_users/')
        self.assertEqual(response.status_code, 200)
        assert '.csv' in response['Content-Disposition']