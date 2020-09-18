from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


""" IF YOU CHANGE URL MUST CHANGE IN LIST PAGES"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', include('base.urls')),
    path('coo/', include('adminusers.urls')),  # admin = Chief Operating Officer (COO)
    path('', include('accounts.urls')),
    path('department/', include('departments.urls')),
    path('team/', include('teams.urls')),
    path('member/', include('members.urls')),

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
