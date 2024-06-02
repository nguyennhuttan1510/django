from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from common.exceptions.model import ResponseBase
from resource.models import Resource
from resource.serializers import ResourceSerializer


# Create your views here.
class ResourceViewSet(APIView):
    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        file_instances = []
        for file in files:
            file_instance = Resource(file=file)
            file_instance.save()
            file_instances.append(file_instance)
        serializers = ResourceSerializer(file_instances, many=True)
        return Response(ResponseBase(message='Files uploaded', data=serializers.data).get(), status=status.HTTP_201_CREATED)


    # queryset = Resource.objects.all()
    # serializer_class = ResourceSerializer
    # parser_classes = [MultiPartParser]

    # @action(['POST'], detail=False)
    # def upload_single_file(self, request, *args, **kwargs):
    #     serializer = ResourceSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     file = serializer.validated_data['file']
    #     Resource.objects.create(file=file)
    #     print(f'File {file} uploaded')
    #     return Response(ResponseBase(message='File uploaded').get(), status=status.HTTP_201_CREATED)

    # @action(['POST'], detail=False)
    # def upload_multiple_files(self, request, *args, **kwargs):
    #     files = request.FILES.getlist('file')
    #     for f in files:
    #         file_instance = Resource(file=f)
    #         file_instance.save()
    #     return HttpResponse('Files uploaded successfully')
        # file_list = []
        # for file in files:
        #     file_list.append(Resource(file=file))
        # print(f'file_list: {file_list}')
        # if not file_list:
        #     return Response(ResponseBase(message='Files upload failed').get(), status=status.HTTP_400_BAD_REQUEST)
        # Resource.objects.bulk_create(file_list)
        # return Response(ResponseBase(message='Files uploaded').get(), status=status.HTTP_201_CREATED)
