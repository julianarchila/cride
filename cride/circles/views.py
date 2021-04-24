""" Circle views. """

# Django 
from django.http import HttpResponse

# Models
from cride.circles.models import Circle

def list_circles(request):
    circles = Circle.objects.all()
    public = circles.filter(is_public=True)
    data = []
    for circle in public:
        print(circle)

    return HttpResponse("Hello")