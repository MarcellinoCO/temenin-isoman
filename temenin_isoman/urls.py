"""temenin_isoman URL Configuration

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
from django.urls import include, path
from obat import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('obat/', include('obat.urls')),
    path('', include('django.contrib.auth.urls')),

    path('bed-capacity/', include('bed_capacity.urls')),
    path('checklist/', include('checklist.urls')),
    path('deteksimandiri/', include('deteksimandiri.urls')),
    path('emergency-contact/', include('emergency_contact.urls')),
    path('happy-notes/', include('happy_notes.urls')),
    path('obat/', include('obat.urls')),
    path('tips-and-tricks/', include('tips_and_tricks.urls')),
    path('user/', include('user.urls')),
]
