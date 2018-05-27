from django.db import models


# Create your models here.
class URLBlacklist(models.Model):
    url = models.CharField(max_length=500, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'url_blacklist'
