from django.test import TestCase
from ..forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        data = {'first_name': 'first_name', 'last_name': 'last_name', 'email': 'user@test.com', 
                'username': 'user', 'password1': 'SecurePass!2024', 'password2': 'SecurePass!2024'}
        form = CustomUserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'email': 'user@@test.com'}
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

class CustomUserChangeFormTest(TestCase):
    def test_valid_form(self):
        data = {'first_name': 'first_name', 'last_name': 'last_name', 
                'username': 'user', 'email': 'user@test.com'}
        form = CustomUserChangeForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'email': 'user@@test.com'}
        form = CustomUserChangeForm(data=data)
        self.assertFalse(form.is_valid())
