from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from user.models import User


class PrintJob(models.Model):
    """
    Model for Print Jobs
    """

    DIMENSION_CHOICES = [
        ('in', 'inches'),
        ('cm', 'centimeters'),
        ('mm', 'millimeters')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    accepted_vendor_offer = models.OneToOneField(
        'VendorOffer', on_delete=models.PROTECT, blank=True, null=True)
    budget = models.IntegerField(validators=[MinValueValidator(0)])
    completed = models.BooleanField(default=False)
    details = models.TextField()
    dimension_unit = models.CharField(choices=DIMENSION_CHOICES, max_length=2)
    filament = models.CharField(max_length=150, blank=False)
    fill = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)])
    name = models.CharField(max_length=150, blank=False)
    model = models.URLField()
    modeler = models.ForeignKey(User, on_delete=models.CASCADE)
    primary_image = models.URLField()
    print_dimension_x = models.IntegerField(validators=[MinValueValidator(0)])
    print_dimension_y = models.IntegerField(validators=[MinValueValidator(0)])
    print_dimension_z = models.IntegerField(validators=[MinValueValidator(0)])
    street_address = models.CharField(max_length=1000, blank=False)
    city = models.CharField(max_length=1000, blank=False)
    state = models.CharField(max_length=1000, blank=False)
    zip_code = models.CharField(max_length=10)


class ModelImage(models.Model):
    """
    Model for Additional PrintJob Model Images
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    image = models.URLField()
    print_job = models.ForeignKey(
        PrintJob, on_delete=models.CASCADE, related_name='additional_images')


class VendorOffer(models.Model):
    """
    Model for Offers on Print Jobs made by Vendors
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    print_job = models.ForeignKey(
        PrintJob, on_delete=models.CASCADE, related_name='vendor_offers')
    bid = models.IntegerField(validators=[MinValueValidator(0)])
    details = models.TextField()
