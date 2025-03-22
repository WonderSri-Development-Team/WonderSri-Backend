from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="WonderSri Location API",
        default_version="v1",
        description="API documentation for location-related endpoints",
        contact=openapi.Contact(email="wondersriteam@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)
