from django.urls import path

from url_lookup.views import URLInfoView, URLCheckView

url_info_view = URLInfoView.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update'
})
urlpatterns = [
    path('1/<str:host>/<str:path>', URLCheckView.as_view(),
         name='Get URL Info'),
    path('url/', url_info_view, name='Add/Update/List URLs')
]
