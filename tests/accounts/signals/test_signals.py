from django.contrib.auth import get_user_model
from django.test import TestCase

from HairSaloon.accounts.models import Profile
from HairSaloon.hairdressers.models import HairDresser

UserModel = get_user_model()


class UserSignalsTest(TestCase):

    def test_profile_creation_on_user_creation(self):
        user = UserModel.objects.create_user(email='user@example.com', password='password')
        self.assertTrue(Profile.objects.filter(user=user).exists(), "Profile should be created for new users.")

    def test_hairdresser_creation_for_staff_user(self):
        staff_user = UserModel.objects.create_user(email='staff@example.com', password='password')
        staff_user.is_staff = True
        staff_user.save()
        self.assertTrue(HairDresser.objects.filter(user=staff_user).exists(),
                        "HairDresser should be created for staff users.")

    def test_hairdresser_deletion_for_non_staff_user(self):
        staff_user = UserModel.objects.create_user(email='staff@example.com', password='password')
        staff_user.is_staff = True
        staff_user.save()
        self.assertTrue(HairDresser.objects.filter(user=staff_user).exists(),
                        "HairDresser should be created for staff users.")
        staff_user.is_staff = False
        staff_user.save()
        self.assertFalse(HairDresser.objects.filter(user=staff_user).exists(),
                         "HairDresser should be deleted for non-staff users.")

    def test_no_action_for_superuser(self):
        superuser = UserModel.objects.create_superuser(email='superuser@example.com', password='password')

        self.assertTrue(superuser.is_superuser, "Superuser should be created correctly.")
        self.assertFalse(HairDresser.objects.filter(user=superuser).exists(),
                         "No HairDresser should be created for superusers.")
        self.assertTrue(Profile.objects.filter(user=superuser).exists(),
                        "Profile should be created for superusers.")
