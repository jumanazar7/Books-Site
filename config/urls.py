from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as drf_schema_view
from drf_yasg import openapi
from rest_framework import permissions, authentication


schema_view = drf_schema_view(
    openapi.Info(
        title='API ning sarlavhasi',
        default_version="v1",
        description="API ning descriptioni",
        terms_of_service="https://policies.google.com/terms",\
        contact=openapi.Contact(email="bekzod@gmail.com"),
        license=openapi.License(name="Bez litsenziya")
    ),
    public=True,
    permission_classes = (permissions.AllowAny,),
    authentication_classes=(authentication.BasicAuthentication, authentication.SessionAuthentication, authentication.TokenAuthentication)
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
    path('api/v1/', include('api.urls')),
    path('api/v1/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/v1/dj-rest-auth/register/', include('dj_rest_auth.registration.urls')),
    path('main/', include('main.urls')),
    path('auth/', include('accounts.urls', namespace='auth')),
    path('rest-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('accounts/', include('django.contrib.auth.urls'))
    # path('password/reset/', views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password_reset"),
    path('password/reset/done/', views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'), 
    path('openapi/', get_schema_view(
        title="Bu API ning sarlavhasi",
        description="API ning tasnifi",
        version="1.0.0"
    ), name="openapi-schema"),
    path('swagger/', schema_view.with_ui("swagger", cache_timeout=0), name="swagger-doc"),
    path('redoc/', schema_view.with_ui("redoc", cache_timeout=0), name="redoc-doc")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

