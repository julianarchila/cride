""" Invitations tests. """

# Django
from django.test import TestCase, client

# Models
from cride.circles.models import Invitation
from cride.users.models import User 

class InviationsManagerTestCase(TestCase):
    """ Inviations manager test case. """
    def setUp(self):
        """ Test case setup. """
        self.user = User.objects.create(
            first_name="Julian",
            last_name="Archila",
            email="julialejo2018@gmail.com"
        )