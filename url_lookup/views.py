import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from .controllers import URLInfo


class URLInfoView(viewsets.ModelViewSet):
    def get(self, request, *args, **kwargs):
        """
        Retrieve URL Info and adding new URLs to be blacklisted
        :param request:
        :param args:
        :param kwargs:
        :return:
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

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        """
        Adds a new URL to the Malware URL List in the DataBase
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = json.loads(request.body)
        is_inserted = URLInfo.insert(URLInfo(), data)
        if is_inserted:
            response = {
                'status': 'success',
                'message': 'Inserted successfully'
            }
            return JsonResponse(response)

        else:
            error_response = {
                'status': 'error',
                'message': 'Invalid data'
            }
            return JsonResponse(error_response, status=400)
