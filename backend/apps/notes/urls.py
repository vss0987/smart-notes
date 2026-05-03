"""
Маршрутизация URL для заметок через ViewSet.
"""
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet

router = DefaultRouter()
router.register("notes", NoteViewSet, basename="notes")

urlpatterns = router.urls