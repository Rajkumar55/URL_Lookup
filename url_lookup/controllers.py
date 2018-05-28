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
            try:
                url_info = URLBlacklist.objects.get(url__iexact=data['host_name'])
                if url_info.is_active:
                    return False, 'Already Available'
            except URLBlacklist.DoesNotExist as e:
                URLBlacklist.objects.create(url=data['host_name'], is_active=True)
                return True, 'Inserted successfully'
        else:
            return False, None
