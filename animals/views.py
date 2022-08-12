from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Request, Response, status
from animals import serializers

from animals.models import Animal
from animals.serializers import (
    AnimalByIdSerializer,
    AnimalSerializer,
    CustomValidationError,
)


class AnimalsView(APIView):
    def get(self, request: Request) -> Response:
        animals = Animal.objects.all()
        animals_serializer = AnimalSerializer(animals, many=True)
        # import ipdb
        # ipdb.set_trace()
        return Response(animals_serializer.data)

    def post(self, request: Request) -> Response:
        animal = AnimalByIdSerializer(data=request.data)

        # import ipdb
        # ipdb.set_trace()
        animal.is_valid(raise_exception=True)
        animal.save()

        return Response(animal.data, status.HTTP_201_CREATED)


class AnimalWithIpView(APIView):
    def get(self, request: Request, animal_id: int):
        animal = get_object_or_404(Animal, id=animal_id)
        animal_serializer = AnimalByIdSerializer(animal)

        return Response(animal_serializer.data)

    def patch(self, request: Request, animal_id: int):
        animal = get_object_or_404(Animal, id=animal_id)

        animal_serializer = AnimalByIdSerializer(
            animal, data=request.data, partial=True
        )
        animal_serializer.is_valid(raise_exception=True)

        try:
            animal_serializer.save()
        except CustomValidationError as errors:
            return Response(errors.args[0], status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(animal_serializer.data)

    def delete(self, request: Request, animal_id):
        animal = get_object_or_404(Animal, id=animal_id)

        animal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# EOF
