"""data_visualizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
<<<<<<< HEAD
from django.urls import path, include
=======
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from reporting_website import views as uploader_views
>>>>>>> a54b7a94a1f0b74208c7a4dbcf2b6e362c95a73e

urlpatterns = [
    path('', include('reporting_website.urls')),
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include('reporting_website.urls')),
]
=======
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> a54b7a94a1f0b74208c7a4dbcf2b6e362c95a73e
