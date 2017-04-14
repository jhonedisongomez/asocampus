from django.conf.urls import url
from .views import ProfileView

urlpatterns = [
    """
    url(r'^consultar-escarapela/$', SearchIdCardPdfView.as_view(),name='search-id-card'),
    url(r'^descargar-escarapela/$', DownloadIdCardPdfView.as_view(),name='download-id-card'),
    url(r'^renovacion-escarapela/$', IdCardView.as_view(),name='renovate-id-card'),

    """
    url(r'^mi-perfil/$', ProfileView.as_view(),name='my-profile'),
]
