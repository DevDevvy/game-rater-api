"""gamerater URL Configuration

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
from django.contrib import admin
from django.urls import include, path
# import rest framework
from rest_framework import routers
# import all views for routing
from gameraterapi.views import GameView
from gameraterapi.views.Gamer import GamerView
from gameraterapi.views.auth import login_user, register_user
from gameraterapi.views.category import CategoryView
from gameraterapi.views.gamereview import GameReviewView
from gameraterapi.views.photo import PhotoView
from gameraterapi.views.rating import RatingView
from django.conf.urls.static import static
from django.conf import settings
# make url not need trailing slash to work
router = routers.DefaultRouter(trailing_slash=False)
# ----------------url, what view, basename for errors
router.register(r'games', GameView, 'game')
router.register(r'categories', CategoryView, 'category')
router.register(r'reviews', GameReviewView, 'review')
router.register(r'gamers', GamerView, 'gamer')
router.register(r'ratings', RatingView, 'rating')
router.register(r'photos', PhotoView, 'photo')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ^last line is for photo media settings to be tied to a URL