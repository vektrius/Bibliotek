"""Bibliotek URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Bibliotek import settings
from UserApp.views import RegistrationView, LoginView, BooksView, BookInfoView, rate_system_view
from django.views.generic import RedirectView

urlpatterns = [
                  path('', RedirectView.as_view(pattern_name='registration'), name="main-page"),
                  path('admin/', admin.site.urls),
                  path('registration/', RegistrationView.as_view(), name='registration'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('books/', BooksView.as_view(), name='books'),
                  path('book/<int:pk>', BookInfoView.as_view(), name='book'),
                  path('test/', rate_system_view, name='test')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
