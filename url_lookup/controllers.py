from .models import URLBlacklist


class URLInfo(object):
    def get_info(self, host_name):
        try:
            url_blacklist_obj = URLBlacklist.objects.get(url__iexact=host_name, is_active=True)
            return True
        except URLBlacklist.DoesNotExist as e:
            print('URL does not exist in the table')
            return False

    def insert(self, data):
        if data['host_name']:
            URLBlacklist.objects.create(url=data['host_name'], is_active=True)
            return True
        else:
            return False
