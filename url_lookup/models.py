from django.db import models


# Create your models here.
class URLBlacklist(models.Model):
    url = models.CharField(max_length=100, null=False, blank=False, unique=True)
    is_restricted = models.BooleanField(default=True, help_text='configuration to allow/restrict the url')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'url_blacklist'
