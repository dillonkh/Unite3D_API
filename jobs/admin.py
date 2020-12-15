from django.contrib import admin

from jobs.models import ModelImage, PrintJob, VendorOffer


admin.site.register(PrintJob)
admin.site.register(ModelImage)
admin.site.register(VendorOffer)
