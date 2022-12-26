"""exchange_mapper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = 'Exchange Mapper Administration'
admin.site.site_title = 'Exchange Mapper Admin Portal'
admin.site.index_title = 'Welcome to Exchange Mapper Admin Portal'

handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'
handler403 = 'main.views.error_403'
handler400 = 'main.views.error_400'

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('', include(('sso.urls', 'sso'), namespace='sso')),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
