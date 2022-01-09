from django.urls import path
from applications.purchase.views import *

app_name = "compra"

urlpatterns = [
    path('providers/', ProviderListView.as_view(), name="provider_list"),
    path('new/provider/', ProviderCreateView.as_view(), name="provider_new"),
    path('edit/provider/<int:id_provider>', provider_edit, name="provider_edit"),
    path('delete/provider/<int:pk>', ProviderDeleteView.as_view(), name="provider_delete"),
    path('edit/provider/state/<int:id_provider>', provider_state, name="provider_estado"),
]
