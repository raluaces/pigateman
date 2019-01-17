from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf.urls import url
from pigateman.settings import STATIC_URL, BASE_DIR

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(
        url=STATIC_URL + 'favicon.ico'
    )),
    path('admin/', admin.site.urls),
    path('door/', include('doorctl.urls'))
]
