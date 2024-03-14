from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from organization.models import Organization
from organization.serializers import OrganizationSerializer


# Create your views here.
@api_view(['GET'])
def view_organization(request, pk=None):
    # checking for the parameters from the URL
    if pk is not None:
        obj = get_object_or_404(Organization, pk=pk)
        instance = OrganizationSerializer(obj, many=False).data
        return Response(instance)

    if request.query_params:
        items = OrganizationSerializer.objects.filter(**request.query_params.dict())
    else:
        items = Organization.objects.all()

    if items:
        instance = OrganizationSerializer(items, many=True).data
        return Response(instance, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
