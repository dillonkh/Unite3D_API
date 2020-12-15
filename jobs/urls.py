from django.urls import path
from jobs import views

urlpatterns = [
    path('accept-offer', views.accept_vendor_offer),
    path('bid', views.VendorOfferList.as_view()),
    path('completed', views.mark_print_job_completed),
    path('list', views.PrintJobList.as_view()),
    path('details/<uuid:print_job_id>', views.PrintJobDetail.as_view()),
    path('details/<uuid:print_job_id>/offers', views.VendorOfferList.as_view())
]
