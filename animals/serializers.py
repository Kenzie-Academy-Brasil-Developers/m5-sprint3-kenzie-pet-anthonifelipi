import math
from black import LN
from django.forms import IntegerField
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from traits.serializers import TraitSerializer
from .models import Animal, SexAnimal
from groups.serializers import GroupSerializer
from groups.models import Group
from traits.models import Trait


class CustomValidationError(Exception):
    ...

class AnimalSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexAnimal.choices,
        default=SexAnimal.DEFAULT,
    )
    age_in_human_years = serializers.SerializerMethodField()
    group = GroupSerializer(read_only=True)
    traits = TraitSerializer(read_only=True, many=True)

    def get_age_in_human_years(self, obj: Animal):
        human_years = 16 * math.log(obj.age) + 31
        return round(human_years)


class AnimalByIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexAnimal.choices,
        default=SexAnimal.DEFAULT,
    )
    age_in_human_years = serializers.SerializerMethodField()
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def get_age_in_human_years(self, obj: Animal):
        human_years = 16 * math.log(obj.age) + 31
        return round(human_years)

    def create(self, validated_data: dict):
        group_data = validated_data.pop("group")
        traits_data = validated_data.pop("traits")

        new_group, _ = Group.objects.get_or_create(**group_data)

        new_animal = Animal.objects.create(**validated_data, group=new_group)

        for trait in traits_data:
            new_trait, _ = Trait.objects.get_or_create(**trait)
            new_animal.traits.add(new_trait)

        new_animal.save()

        return new_animal

    def update(self, instance: Animal, validated_data) -> Animal:
        list = ["group", "traits", "sex"]
        errors = {}
        for key, value in validated_data.items():
            if key in list:
                errors[key] = f"You cannot update {key} property"
                continue
            setattr(instance, key, value)
        if errors:
            raise CustomValidationError(errors)

        instance.save()
        return instance
