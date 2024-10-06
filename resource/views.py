import boto3
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
# from rest_framework.decorators import action
# from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from common.exceptions.model import ResponseBase
from resource.models import Resource, PrivateDocument
from resource.serializers import ResourceSerializer, PrivateDocumentSerializer


def get_presigned_url(key):
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    s3_client = session.client('s3')
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key},
        ExpiresIn=3600  # URL expires in 1 hour
    )
    return url


# Create your views here.
class ResourceViewSet(viewsets.ModelViewSet):
    queryset = PrivateDocument.objects.all()
    serializer_class = PrivateDocumentSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @action(detail=True, methods=['GET'])
    def presigned_url(self, request, *args, **kwargs):
        document = get_object_or_404(PrivateDocument, id=kwargs['pk'])
        #NOTE: key = [path_name_document]/[document_name] => private/media/image_001.png
        path_name = settings.AWS_PRIVATE_MEDIA_LOCATION
        key = f'{path_name}/{document.upload.name}'
        file_url = get_presigned_url(key)
        return Response({'file_url': file_url})

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        file_instances = []
        for file in files:
            file_instance = PrivateDocument(upload=file)
            file_instance.save()
            file_instances.append(file_instance)
        serializers = PrivateDocumentSerializer(file_instances, many=True)
        return Response(ResponseBase(message='Files uploaded', data=serializers.data).get(),
                        status=status.HTTP_201_CREATED)

    # def retrieve(self, request, *args, **kwargs):
    #     document = get_object_or_404(PrivateDocument, id=kwargs['pk'])
    #     file_url = self.get_private_file_url(document.upload.name)
    #     return Response(ResponseBase(message='Get documents success', data=file_url).get(), status=status.HTTP_200_OK)
