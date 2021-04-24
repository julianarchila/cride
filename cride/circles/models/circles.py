""" Circle model. """

# Djnago
from django.db import models

# Utilities
from cride.utils.models import CRideModel

class Circle(CRideModel):
    """Circle model.

    A circle is a private group where rides are offered and taken
    by its members. To join a circles users must recive a unique
    invitation code from a existing circle member.
    """
    pass
    "name, slug name  about, picture, rides_taken, rides_offered"
    name = models.CharField("circle name", max_length=140)
    slug_name = models.CharField(unique=True, max_length=40)

    about = models.CharField("circle description", max_length=255)
    picture = models.ImageField(upload_to="circles/pictures", blank=True, null=True)

    # Stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(
        "verified circle",
        default=False,
        help_text="Verified circles are also known as official comunities."
    )
    
    is_public = models.BooleanField(
        default=False,
        help_text="Public circles are listed in the main page so everyone know about their existence."
# def import_data(file):
#     with open(str(file)) as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         line_counter = 0
#         for row in csv_reader:
#             if line_counter != 0:
#                 c = Circle(
#                     name=row[0],
#                     slug_name=row[1],
#                     rides_offerted=int(row[2]),
#                     rides_taken=int(row[3]),
#                     is_limited=(False if int(row[4]) == 0 else True),
#                     members_limit=int(row[4])
#                 )
#                 c.save()
#             line_counter += 1
# import_data('circles.csv')
    )
    
    is_limited = models.BooleanField(
        "limited", 
        default=False,
        help_text="Limited circles can grow to a fixed number of members."
    )
    members_limit = models.PositiveIntegerField(
        default=0,
        help_text="If circle is limited, this will be the limit on the number of members."
    )

    def __str__(self):
        return self.name

    class Meta(CRideModel.Meta):
        ordering = ["-rides_taken", "-rides_offered"]
