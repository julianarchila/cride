""" Invitations tests. """

# Django
from cride.users.models.profiles import Profile
from django.test import TestCase, client

# Django REST framework
from rest_framework.test import APITestCase

# Models
from cride.circles.models import Invitation
from cride.users.models import User
from cride.circles.models import Circle, Membership
from rest_framework.authtoken.models import Token


class InviationsManagerTestCase(TestCase):
    """Inviations manager test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name="Julian",
            last_name="Archila",
            email="julialejo2018@gmail.com",
            username="julialejo",
            password="admin123",
        )
        self.circle = Circle.objects.create(
            name="Test Circle",
            slug_name="test-circle",
            about="About circle",
            verified=True,
        )

    def test_code_generation(self):
        """Test code generation."""
        invitation = Invitation.objects.create(issued_by=self.user, circle=self.circle)
        self.assertIsNotNone(invitation.code)

    def test_code_usage(self):
        """If code is given, there is no need to create a new one."""
        code = "holamundo"
        invitation = Invitation.objects.create(
            issued_by=self.user, circle=self.circle, code=code
        )

        self.assertEqual(invitation.code, code)

    def test_code_generation_if_duplicated(self):
        """If given code is not unique,a new one is generated."""
        code = Invitation.objects.create(issued_by=self.user, circle=self.circle).code

        # create a new invitationn with the past code
        invitation = Invitation.objects.create(
            issued_by=self.user, circle=self.circle, code=code
        )

        self.assertNotEqual(code, invitation.code)


class MemberInvitationsApiTestCase(APITestCase):
    """Invitations API test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name="Julian",
            last_name="Archila",
            email="julialejo2018@gmail.com",
            username="julialejo",
            password="admin123",
        )
        self.profile = Profile.objects.create(user=self.user)
        self.circle = Circle.objects.create(
            name="Test Circle",
            slug_name="test-circle",
            about="About circle",
            verified=True,
        )
        self.membership = Membership.objects.create(
            user=self.user,
            profile=self.profile,
            circle=self.circle,
            remaining_invitations=10,
        )

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        # URL
        self.url = f"/circles/{self.circle.slug_name}/members/{self.user.username}/invitations/"

    def test_response_success(self):
        """Verify request succeded."""
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)

    def test_invitations_creation(self):
        """Verify invitations are created if there were no invitations before."""

        # invitations in db must be 0
        self.assertEqual(Invitation.objects.count(), 0)

        # call the endpoint
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)

        # verify invitations where created
        invitations = Invitation.objects.filter(issued_by=self.user, circle=self.circle)
        # check number of invitations is equal to remaining invitations in membership
        self.assertEqual(invitations.count(), self.membership.remaining_invitations)

        # check each invitation code exists in request.data["invitations"]
        for invitation in invitations:
            self.assertIn(invitation.code, request.data["invitations"])
