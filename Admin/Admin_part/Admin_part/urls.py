from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('', include('web_admin.urls', namespace='web_admin')),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

handler404 = 'core.views.page_not_found'

handler500 = 'core.views.server_error'

handler403 = 'core.views.permission_denied'
