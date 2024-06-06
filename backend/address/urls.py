from django.urls import path

from . import views

urlpatterns = [
    path("addresses/",
         views.AddressView.as_view(http_method_names=['get','post']), name="addresses"),

    path("addresses/<uuid>/", views.AddressDetailView.as_view(
        http_method_names=['get', 'put']), name="address-detail"),
]
