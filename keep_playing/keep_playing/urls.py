"""keep_playing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.urls import include, path
from . import views

from django.contrib import admin

#the two lines below are to allow the application to access media files 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('sheetreader/', include('sheetreader.urls')),
]


#adds media files to urlpatterns (giving the website access to them)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
