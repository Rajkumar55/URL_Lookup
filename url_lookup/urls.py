from django.urls import path

from url_lookup.views import URLInfoView

url_info_view = URLInfoView.as_view({
    'get': 'get',
    'post': 'create'
})
urlpatterns = [
    path('1/<str:host>/<str:path>', url_info_view,
         name='Get URL Info'),
    path('add/', url_info_view, name='Add new URL')
]
