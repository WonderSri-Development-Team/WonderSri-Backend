"""
URL configuration for WonderSri_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from users.swagger import schema_view
from users import views

urlpatterns = [
    path('login',views.login),

    re_path('signup',views.signup),
    path('request-password-reset',views.request_password_reset),

    path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset-password'),

    path('change-password',views.change_password),

    path('test-auth',views.test_auth),

    path('logout',views.logout),

    path('google-login', views.googleoauthlogin),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),

    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='swagger-schema'),

    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    
    path('profile/', get_profile, name='get profile'),
    path('profile/update/', update_profile, name='update profile'),

]