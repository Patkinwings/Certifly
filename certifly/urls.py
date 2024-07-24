from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from core.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # This includes all URLs from core app, including the home view
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]

# Add this at the end of the file
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)