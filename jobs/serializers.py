from rest_framework import serializers
from jobs.models import ModelImage, PrintJob, VendorOffer
from user.serializers import UserSerializer


class VendorOfferSerializer(serializers.ModelSerializer):
    """
    Defines JSON serialization and deserialization for PrintJob Model
    """

    class Meta:
        model = VendorOffer
        fields = '__all__'


class ModelImageSerializer(serializers.ModelSerializer):
    """
    Defines JSON serialization and deserialization for ModelImage Model
    """

    class Meta:
        model = ModelImage
        fields = '__all__'


class PrintJobSerializer(serializers.ModelSerializer):
    """
    Defines JSON serialization and deserialization for PrintJob Model
    """

    vendor_offers = VendorOfferSerializer(many=True, required=False)

    class Meta:
        model = PrintJob
        fields = '__all__'


class PrintJobWithAdditionalImagesSerializer(serializers.ModelSerializer):
    """
    Defines JSON serialization and deserialization for PrintJob Model
    """

    vendor_offers = VendorOfferSerializer(many=True, required=False)
    additional_images = ModelImageSerializer(many=True, required=False)

    class Meta:
        model = PrintJob
        fields = '__all__'


class PrintJobGeneralDetailsSerializer(serializers.ModelSerializer):
    """
    Defines JSON serialization and deserialization for PrintJob Model
    """

    additional_images = ModelImageSerializer(many=True)

    class Meta:
        depth = 1
        model = PrintJob
        fields = ['details', 'primary_image',
                  'additional_images', 'accepted_vendor_offer']


class PrintJobVendorDetailsSerializer(serializers.ModelSerializer):
    """
    Defines JSON serialization and deserialization for PrintJob Model
    """

    modeler = UserSerializer()

    class Meta:
        model = PrintJob
        fields = ['modeler', 'street_address',
                  'city', 'state', 'zip_code', 'model']
