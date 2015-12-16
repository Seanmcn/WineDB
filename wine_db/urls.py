from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  url(r'data.json', views.json_file, name='json')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
