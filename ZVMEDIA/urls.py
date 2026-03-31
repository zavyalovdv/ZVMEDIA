"""
URL configuration for ZVMEDIA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from ZVMEDIA import settings
from booklibrary import views as book_views
from musiclibrary import views as music_views
from movielibrary import views as movie_views
from users import views as users_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", include("booklibrary.urls")),
    path("musics/", include("musiclibrary.urls")),
    path("movies/", include("movielibrary.urls")),
    path("users/", include("users.urls")),
    path("login/", users_views.userlogin, name="login"),
    path("logout/", users_views.userlogout, name="logout"),
    path("", users_views.index, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler_404 = page_not_found
