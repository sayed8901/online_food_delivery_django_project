from django.contrib import admin
from django.urls import path, include

# necessary importing for media files
from django.conf import settings
from django.conf.urls.static import static

# for swagger API
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('accounts.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),


    path("api-auth/", include("rest_framework.urls")),

    # OpenAPI schema generation endpoint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc UI
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]



# defining media urls by adding onto the urlpatterns
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
