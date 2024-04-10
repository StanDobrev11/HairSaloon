from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

UserModel = get_user_model()


class HairSaloonUserManagerTests(TestCase):

    def test_create_user(self):
        user = UserModel.objects.create_user(email='normal@user.com', password='foo')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('foo'))
        self.assertEqual(user.email, 'normal@user.com')

    def test_create_superuser(self):
        admin_user = UserModel.objects.create_superuser('super@user.com', 'foo')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_create_superuser_with_wrong_flags(self):
        with self.assertRaises(ValueError):
            UserModel.objects.create_superuser(email='super@wrong.com', password='foo', is_staff=False)
        with self.assertRaises(ValueError):
            UserModel.objects.create_superuser(email='super@wrong.com', password='foo', is_superuser=False)


class UserManagerWithPermTest(TestCase):

    def setUp(self):
        # Create a permission
        content_type = ContentType.objects.get_for_model(UserModel)
        self.permission = Permission.objects.create(
            codename='test_permission',
            name='Test Permission',
            content_type=content_type,
        )

        # Create two users, one with the permission and one without
        self.user_with_perm = UserModel.objects.create_user(email='user_with_perm@example.com', password='password')
        self.user_with_perm.user_permissions.add(self.permission)
        self.user_with_perm.save()

        self.user_without_perm = UserModel.objects.create_user(email='user_without_perm@example.com',
                                                               password='password')

    def test_with_perm_includes_user_with_permission(self):
        # Fetch users with the test permission
        users_with_perm = UserModel.objects.with_perm('accounts.test_permission')

        # Check that the user with the permission is included
        self.assertIn(self.user_with_perm, users_with_perm)

    def test_with_perm_excludes_user_without_permission(self):
        # Fetch users with the test permission
        users_with_perm = UserModel.objects.with_perm('accounts.test_permission')

        # Check that the user without the permission is not included
        self.assertNotIn(self.user_without_perm, users_with_perm)

    def test_with_perm_superusers_included(self):
        # Create a superuser
        superuser = UserModel.objects.create_superuser(email='superuser@example.com', password='password')

        # Fetch users with the test permission, including superusers
        users_with_perm = UserModel.objects.with_perm('accounts.test_permission', include_superusers=True)

        # Check that the superuser is included
        self.assertIn(superuser, users_with_perm)

    def test_with_perm_active_filter(self):
        # Deactivate the user with permission
        self.user_with_perm.is_active = False
        self.user_with_perm.save()

        # Fetch active users with the test permission
        users_with_perm = UserModel.objects.with_perm('accounts.test_permission', is_active=True)

        # Check that the deactivated user is not included
        self.assertNotIn(self.user_with_perm, users_with_perm)
