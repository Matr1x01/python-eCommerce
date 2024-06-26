from django.urls import path

from . import views

urlpatterns = [
    path("apply-coupon/",
         views.CouponApplyView.as_view(http_method_names=['post']), name="apply-coupon"),
]