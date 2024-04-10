from django.test import TestCase
from HairSaloon.accounts.models import HairSaloonUser, Profile, user_directory_path


class HairSaloonUserModelTest(TestCase):

    def test_full_name_property_full_name(self):
        user = HairSaloonUser(first_name="John", last_name="Doe", email="john@example.com")
        self.assertEqual(user.full_name, "John Doe")

    def test_full_name_property_partial_name(self):
        user = HairSaloonUser(first_name="John", email="john@example.com")
        self.assertEqual(user.full_name, "John")

    def test_full_name_property_no_name(self):
        user = HairSaloonUser(email="john@example.com")
        self.assertEqual(user.full_name, "john@example.com")


class UserProfileModelTest(TestCase):

    def test_user_directory_path(self):
        user = HairSaloonUser(pk=1)  # Assuming the user's ID is 1
        path = user_directory_path(instance=Profile(user=user), filename='mypic.jpg')
        self.assertEqual(path, "user_1/mypic.jpg")
