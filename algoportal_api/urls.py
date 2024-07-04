from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as get_swagger_schema_view

from .router import router
from main import urls


schema_view = get_swagger_schema_view(
    openapi.Info(
        title='Algoportal API',
        default_version='1.0.0',
        description='API documentation of App',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(urls.urlpatterns)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
]
