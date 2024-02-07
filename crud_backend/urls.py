from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from todo.views import TodoViewSet
from userprofile.views import AuthViewSet

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]