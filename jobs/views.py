from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from jobs.models import PrintJob, VendorOffer
from jobs import serializers


class PrintJobList(APIView):
    """
    View
    """

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Endpoint for Create Print Job
        """
        if request.user.is_vendor:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data['modeler'] = request.user.id
        serializer = serializers.PrintJobSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        print_job = serializer.save()

        for url in request.data['additional_images']:
            print_job.additional_images.create(image=url)

        serializer = serializers.PrintJobWithAdditionalImagesSerializer(
            print_job)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Endpoint for getting Print Jobs
        """
        print_jobs = PrintJob.objects.all()

        if not request.user.is_vendor:
            print_jobs = print_jobs.filter(modeler=request.user)

            if request.query_params:
                query_filter = request.query_params['filter']
                if query_filter == 'offers-pending':
                    print_jobs = print_jobs.filter(
                        accepted_vendor_offer=None, vendor_offers__isnull=False).distinct()
                elif query_filter == 'accepted-incomplete':
                    print_jobs = print_jobs.filter(
                        accepted_vendor_offer__isnull=False, completed=False)
                elif query_filter == 'accepted-complete':
                    print_jobs = print_jobs.filter(
                        accepted_vendor_offer__isnull=False, completed=True)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

        else:
            if request.query_params:
                query_filter = request.query_params['filter']
                if query_filter == 'bids-pending':
                    vendor_offers = VendorOffer.objects.filter(
                        vendor=request.user, print_job__completed=False,
                        print_job__accepted_vendor_offer__isnull=True)
                    print_jobs = []
                    for vendor_offer in vendor_offers:
                        print_jobs.append(vendor_offer.print_job)
                elif query_filter == 'progress-pending':
                    print_jobs = print_jobs.filter(
                        completed=False, accepted_vendor_offer__vendor=request.user)
                elif query_filter == 'completed':
                    print_jobs = print_jobs.filter(
                        completed=True, accepted_vendor_offer__vendor=request.user)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                print_jobs = print_jobs.filter(
                    accepted_vendor_offer__isnull=True)

        serializer = serializers.PrintJobWithAdditionalImagesSerializer(
            print_jobs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PrintJobDetail(APIView):
    """
    View
    """

    def get(self, request, print_job_id, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Endpoint for getting General Job details
        """
        print_job = get_object_or_404(PrintJob, pk=print_job_id)

        if request.user.is_vendor:
            serializer = serializers.PrintJobVendorDetailsSerializer(print_job)
        else:
            serializer = serializers.PrintJobGeneralDetailsSerializer(
                print_job)

        return Response(serializer.data, status.HTTP_200_OK)


@ api_view(['POST'])
def accept_vendor_offer(request):
    """
    Endpoint for accepting a Vendor Offer
    """
    if request.user.is_vendor:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        vendor_offer = VendorOffer.objects.get(pk=request.data['vendor_offer'])
    except VendorOffer.DoesNotExist:
        return Response({'errors': 'No Vendor Offer with ID ' + request.data.vendor_offer}, status=status.HTTP_400_BAD_REQUEST)

    print_job = vendor_offer.print_job
    print_job.accepted_vendor_offer = vendor_offer
    print_job.save()

    return Response(status=status.HTTP_204_NO_CONTENT)


@ api_view(['POST'])
def mark_print_job_completed(request):
    """
    Endpoint for marking a Print Job as completed
    """
    if not request.user.is_vendor:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        print_job = PrintJob.objects.get(pk=request.data['print_job'])
    except PrintJob.DoesNotExist:
        return Response({'errors': 'No Print Job with ID ' + request.data.print_job}, status=status.HTTP_400_BAD_REQUEST)

    print_job.completed = True
    print_job.save()

    return Response(status=status.HTTP_204_NO_CONTENT)


class VendorOfferList(APIView):
    """
    View
    """

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Endpoint for Create Vendor Offer
        """

        if not request.user.is_vendor:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.data['vendor'] = request.user.id

        serializer = serializers.VendorOfferSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request, print_job_id, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Endpoint for getting Vendor Offers for a Print Job
        """
        if request.user.is_vendor:
            return Response(status=status.HTTP_404_NOT_FOUND)

        print_job = get_object_or_404(PrintJob, pk=print_job_id)

        serializer = serializers.VendorOfferSerializer(
            print_job.vendor_offers.all(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
