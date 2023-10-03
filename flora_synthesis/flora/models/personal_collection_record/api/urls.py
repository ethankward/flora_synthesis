from rest_framework import routers

from flora.models.personal_collection_record.api import views


def get_urlpatterns(router: routers.DefaultRouter):
    router.register(
        r"personal_collection_records", views.PersonalCollectionRecordViewSet
    )

    return []
