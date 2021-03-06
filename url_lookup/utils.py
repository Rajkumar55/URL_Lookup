from .models import URLBlacklist


def check_availability(url='', url_id=''):
    if url:
        url_obj = URLBlacklist.objects.filter(url__iexact=url)
        if url_obj:
            return True, url_obj[0]
        else:
            return False, None

    elif url_id:
        url_obj = URLBlacklist.objects.filter(id=url_id)
        if url_obj:
            return True, url_obj[0]
        else:
            return False, None
