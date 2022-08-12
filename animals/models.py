from django.db import models


class SexAnimal(models.TextChoices):
    MALE = "Macho"
    FEMALE = "Femea"
    DEFAULT = "não informado"


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=15,
        choices=SexAnimal.choices,
        default=SexAnimal.DEFAULT,
    )

    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="animals"
    )

    traits = models.ManyToManyField("traits.Trait", related_name="animals")
