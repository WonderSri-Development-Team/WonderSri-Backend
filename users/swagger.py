from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Authentication API",
        default_version="v1",
        description="API documentation for authentication system",
        contact=openapi.Contact(email="wondersriteam@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,  # Allow public access
    permission_classes=[AllowAny],  # Allow unauthenticated users to view API docs
)
