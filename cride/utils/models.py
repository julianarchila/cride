"""Django models utilities """
from django.db import models


class CRideModel(models.Model):
    """ Share Ride base model. 
    CRideModel acts as an abstract class from which every 
    other model in the project will intherit. This class provides 
    every table with the following atributes:
        *Created {DateTime}
        *Modified {DateTime}
    """
    created = models.DateTimeField(
        "created at",
        auto_now_add=True,
        help_text="Date tiem on which the object was created."
    )

    modified = models.DateTimeField(
        "modified at",
        auto_now=True,
        help_text="Date tiem on which the object was last modified."
    )

    class Meta:
        abstract = True
        get_latest_by = "created"
        ordering = ["-created", "-modified"]
