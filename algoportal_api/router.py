from rest_framework import routers

from main.viewsets import recordsViewset


router = routers.DefaultRouter()

router.register('records', recordsViewset) # /api/records