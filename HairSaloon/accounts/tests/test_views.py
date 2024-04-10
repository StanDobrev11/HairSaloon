from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from django.contrib.messages import get_messages
from django.test import TestCase, RequestFactory
from django.urls import reverse

UserModel = get_user_model()


class LoginUserViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='john@example.com',
            password='password',
            first_name='John',
            last_name='Ivanov',
            phone_number='1234'
        )

    def test_redirect_authenticated_user(self):
        self.client.login(email='john@example.com', password='password')
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('index'))

    def test_form_invalid_message(self):
        response = self.client.post(reverse('login'), {'username': 'wrong', 'password': 'user'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid email or password.')


class RegisterUserViewTests(TestCase):

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            email='john@example.com',
            password='password',
            first_name='John',
            last_name='Ivanov',
            phone_number='1234',
        )

    def test_redirect_authenticated_user(self):
        self.client.login(email='john@example.com', password='password')
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('index'))

    def test_activate_soft_deleted_user(self):
        user = self.user
        user.is_active = False
        response = self.client.post(reverse('register'), {
            'email': 'john@example.com',
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'password1': 'NewPassword',
            'password2': 'NewPassword',
            'phone_number': '11223344',
        })
        user.refresh_from_db()
        self.assertTrue(user.is_active)


class HairSalonPasswordChangeViewTests(TestCase):

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            email='john@example.com',
            password='password',
            first_name='John',
            last_name='Ivanov',
            phone_number='1234',
        )

    def test_success_message_on_password_change(self):
        self.client.login(email='john@example.com', password='password')
        url = reverse('password change', kwargs={'pk': self.user.pk})
        response = self.client.post(url, {
            'old_password': 'password',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword',
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Your password has been updated!')


class HairSalonDeleteUserViewTests(TestCase):

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(email='delete@example.com', password='password', is_active=True)

    def test_user_is_deactivated(self):
        self.client.force_login(self.user)
        delete_url = reverse('delete user', kwargs={'pk': self.user.pk})
        self.client.post(delete_url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_user_is_logged_out_on_delete(self):
        self.client.force_login(self.user)
        delete_url = reverse('delete user', kwargs={'pk': self.user.pk})
        self.client.post(delete_url)
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
