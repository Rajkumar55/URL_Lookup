import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import URLBlacklist
from .serializers import URLInfoSerializer
from .controllers import URLInfo
from .utils import check_availability


class URLCheckView(View):
    def get(self, request, *args, **kwargs):
        """
        Retrieve URL Info and adding new URLs to be blacklisted
        :param request:
        :param args:
        :param kwargs:
        :return:

        # Sample Request
            http://localhost:8000/urlinfo/1/example.com:80/test

        # Sample Output

            {
                "host_name": "example.com",
                "port": 80,
                "path": "test",
                "status": "malicious"
            }
        """
        try:
            host = kwargs['host']

            host_name = host
            port = ''
            if ':' in host:
                host_details = host.split(':')
                host_name = host_details[0]
                port = host_details[1]

            path = kwargs.get('path', '')

            is_exists = URLInfo.get_info(URLInfo(), host_name)
            if port:
                port = int(port)

            info = {'host_name': host_name, 'port': port, 'path': path, 'status': 'malicious' if is_exists else 'safe'}
            return JsonResponse(info)

        except Exception as e:
            print('Exception ' + str(e))
            error_response = {
                'status': 'error',
                'message': 'Something went wrong. Please check the request and try again later'
            }
            return JsonResponse(error_response, status=400)


class URLInfoView(viewsets.ModelViewSet):
    model = URLBlacklist
    serializer_class = URLInfoSerializer

    def list(self, request, *args, **kwargs):
        """
        Lists all URLs stored in the DataBase
        :param request:
        :param args:
        :param kwargs:
        :return:

        # Sample Request
            GET http://localhost:8000/urlinfo/url/

        # Sample Response
        {
            "status": "success",
            "data": [
                {
                    "id": 1,
                    "url": "example.com",
                    "is_restricted": true
                },
                {
                    "id": 2,
                    "url": "test.com",
                    "is_restricted": true
                },
                {
                    "id": 3,
                    "url": "hirang.org",
                    "is_restricted": true
                }
            ]
        }
        """
        queryset = self.model.objects.all()
        serializer = URLInfoSerializer(queryset, many=True)
        response = {
            'status': 'success',
            'data': serializer.data
        }
        return JsonResponse(response)

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        """
        Adds a new URL to the Malware URL List in the DataBase
        :param request:
        :param args:
        :param kwargs:
        :return:

        # Sample Request
            POST http://localhost:8000/urlinfo/url/
            {
                "url": "example.us"
            }

        # Sample Response
            {
                "status": "success",
                "message": "Inserted successfully"
            }
        """
        data = json.loads(request.body)
        serializer = URLInfoSerializer(data=data)
        try:
            is_valid = serializer.is_valid(raise_exception=True)
            if is_valid:
                is_exists, url_obj = serializer.save()
                response = {'status': 'success'}
                if is_exists:
                    response['message'] = 'Already Inserted'
                else:
                    response['message'] = 'Inserted successfully'
                return JsonResponse(response)

            else:
                error_response = {
                    'status': 'error',
                    'message': 'Invalid data'
                }
                return JsonResponse(error_response, status=400)

        except Exception as e:
            print(e)
            error_response = {
                'status': 'error',
                'message': str(e)
            }
            return JsonResponse(error_response, status=400)

    @csrf_exempt
    def update(self, request, *args, **kwargs):
        """
        Updates an existing URL
        :param request:
        :param args:
        :param kwargs:
        :return:

        # Sample Request
            PUT http://localhost:8000/urlinfo/url/
            {
                "url_id": 14,
                "url": "example.ru"
            }

        # Sample Response
            {
                "status": "success",
                "message": "Updated successfully"
            }
        """
        data = json.loads(request.body)
        is_exists, url_obj = check_availability(url_id=data['url_id'])
        if is_exists:
            update_data = {
                'id': data['url_id'],
                'url': data['url']
            }
            serializer = URLInfoSerializer(url_obj, data=update_data)
            try:
                is_valid = serializer.is_valid(raise_exception=True)
                if is_valid:
                    serializer.save()
                    response = {'status': 'success', 'message': 'Updated successfully'}
                    return JsonResponse(response)

                else:
                    error_response = {
                        'status': 'error',
                        'message': 'Invalid data'
                    }
                    return JsonResponse(error_response, status=400)

            except Exception as e:
                error_response = {
                    'status': 'error',
                    'message': str(e)
                }
                return JsonResponse(error_response, status=400)
        else:
            error_response = {
                'status': 'error',
                'message': 'URL ID not available'
            }
            return JsonResponse(error_response, status=400)
