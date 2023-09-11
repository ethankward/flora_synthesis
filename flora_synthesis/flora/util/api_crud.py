import typing

from django.urls import path
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


class CRUDViewGenerator:
    def __init__(self, model, model_name: str, creation_function: typing.Callable,
                 update_function: typing.Callable):
        self.model = model
        self.model_name = model_name
        self.creation_function = creation_function
        self.update_function = update_function

    def get_creation_view(self) -> typing.Callable[[Request], Response]:
        @api_view(['PUT'])
        def create_object(request: Request):
            new_object = self.creation_function(request)
            return Response(status=status.HTTP_201_CREATED, data={'object_id': new_object.pk})

        return create_object

    def get_deletion_view(self) -> typing.Callable[[Request], Response]:
        @api_view(['POST'])
        def delete_object(request: Request) -> Response:
            object_id = request.data['object_id']
            print('here', object_id)
            object_to_delete = self.model.objects.get(pk=object_id)
            object_to_delete.delete()

            return Response(status=status.HTTP_200_OK)

        return delete_object

    def get_update_view(self) -> typing.Callable[[Request], Response]:
        @api_view(['POST'])
        def update_object(request: Request) -> Response:
            object_id = request.data['object_id']

            object_to_update = self.model.objects.get(pk=object_id)
            self.update_function(object_to_update, request)
            object_to_update.save()

            return Response(status=status.HTTP_200_OK)

        return update_object

    def get_urlpatterns(self):
        creation_view = self.get_creation_view()
        deletion_view = self.get_deletion_view()
        update_view = self.get_update_view()

        return [
            path('api/create_new_{}/'.format(self.model_name), creation_view),
            path('api/delete_{}/'.format(self.model_name), deletion_view),
            path('api/update_{}/'.format(self.model_name), update_view),
        ]
