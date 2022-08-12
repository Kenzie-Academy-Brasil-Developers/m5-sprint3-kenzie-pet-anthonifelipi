from django.urls import path
from . import views

urlpatterns = [
    path("animals/", views.AnimalsView.as_view()),
    path("animals/<animal_id>/", views.AnimalWithIpView.as_view()),
]

# EOF
