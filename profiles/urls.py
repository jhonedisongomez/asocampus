from django.conf.urls import url
from .views import DownloadIdCardPdfView,SearchIdCardPdfView,IdCardView

urlpatterns = [
    url(r'^consultar-escarapela/$', SearchIdCardPdfView.as_view(),name='search-id-card'),
    url(r'^descargar-escarapela/$', DownloadIdCardPdfView.as_view(),name='download-id-card'),
    url(r'^renovacion-escarapela/$', IdCardView.as_view(),name='renovate-id-card'),

]
