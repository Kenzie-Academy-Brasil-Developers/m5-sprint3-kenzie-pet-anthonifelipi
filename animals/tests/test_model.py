from turtle import right
from django.test import TestCase
from animals.models import Animal
from traits.models import Trait
from groups.models import Group
from faker import Faker

fake = Faker()


class AnimalTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.animal_test = {
            "name": fake.name(),
            "age": fake.pyint(1, 20),
            "weight": fake.pyfloat(min_value=1, max_value=50, right_digits = 1),
            "sex": "DEFAULT",
        }

        cls.group_test = {"name": fake.name(), "scientific_name": "vira-lata"}

        cls.trait_test = {"name": "folgado"}

        cls.group = Group.objects.create(**cls.group_test)
        cls.trait = Trait.objects.create(**cls.trait_test)

        cls.animal = Animal.objects.create(**cls.animal_test, group=cls.group)

        cls.traits = [Trait.objects.create(**{"name": fake.name()}) for _ in range(10)]

    def test_relation_with_traits(self):

        for trait in self.traits:
            self.animal.traits.add(trait)

        self.assertEqual(len(self.traits), self.animal.traits.count())

    def test_relation_with_group(self):
        self.assertIs(self.animal.group, self.group)

    def test_animal_fields(self):

        self.assertEqual(self.animal.name, self.animal_test["name"])
        self.assertEqual(self.animal.age, self.animal_test["age"])
        self.assertEqual(self.animal.weight, self.animal_test["weight"])
        self.assertEqual(self.animal.sex, self.animal_test["sex"])
        self.assertEqual(self.animal.group.name, self.group_test["name"])
        self.assertEqual(
            self.animal.group.scientific_name, self.group_test["scientific_name"]
        )

    def test_group_fields(self):
        self.assertEqual(self.group.name, self.group_test["name"])

    def test_trait_fields(self):
        self.assertEqual(self.trait.name, self.trait_test["name"])


# EOF
