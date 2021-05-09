""" Circle invitations manager. """

# Django
from django.db import models

# Utilities
import random
from string import ascii_uppercase, digits

class InvitationManager(models.Manager):
    """Invitation manager. 
    Used to handle code generation
    """
    CODE_LENGTH = 10
    def create(self, **kwargs):
        pool = ascii_uppercase + digits + ".-"
        code = kwargs.get("code", "".join( random.choices(pool, k=self.CODE_LENGTH)) )
        while self.filter(code=code).exists():
            code = "".join( random.choices(pool, k=self.CODE_LENGTH) )

        kwargs["code"] = code
        return super(InvitationManager, self).create(**kwargs)
        