# from django.shortcuts import render
# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Listing, Booking
# from .serializers import ListingSerializer, BookingSerializer


# class ListingViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for managing Listing objects.
#     Provides CRUD operations (Create, Read, Update, Delete) for property listings.
#     """
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer

#     def list(self, request, *args, **kwargs):
#         """Get all listings"""
#         return super().list(request, *args, **kwargs)

#     def create(self, request, *args, **kwargs):
#         """Create a new listing"""
#         return super().create(request, *args, **kwargs)

#     def retrieve(self, request, *args, **kwargs):
#         """Get a specific listing by ID"""
#         return super().retrieve(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         """Update a listing completely"""
#         return super().update(request, *args, **kwargs)

#     def partial_update(self, request, *args, **kwargs):
#         """Partially update a listing"""
#         return super().partial_update(request, *args, **kwargs)

#     def destroy(self, request, *args, **kwargs):
#         """Delete a listing"""
#         return super().destroy(request, *args, **kwargs)


# class BookingViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for managing Booking objects.
#     Provides CRUD operations (Create, Read, Update, Delete) for bookings.
#     """
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer

#     def list(self, request, *args, **kwargs):
#         """Get all bookings"""
#         return super().list(request, *args, **kwargs)

#     def create(self, request, *args, **kwargs):
#         """Create a new booking"""
#         return super().create(request, *args, **kwargs)

#     def retrieve(self, request, *args, **kwargs):
#         """Get a specific booking by ID"""
#         return super().retrieve(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         """Update a booking completely"""
#         return super().update(request, *args, **kwargs)

#     def partial_update(self, request, *args, **kwargs):
#         """Partially update a booking"""
#         return super().partial_update(request, *args, **kwargs)

#     def destroy(self, request, *args, **kwargs):
#         """Delete a booking"""
#         return super().destroy(request, *args, **kwargs)

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Listing objects.
    Provides CRUD operations (Create, Read, Update, Delete) for property listings.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        """Get all listings"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new listing"""
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Get a specific listing by ID"""
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update a listing completely"""
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Partially update a listing"""
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete a listing"""
        return super().destroy(request, *args, **kwargs)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Booking objects.
    Provides CRUD operations (Create, Read, Update, Delete) for bookings.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        """Get all bookings"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new booking"""
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Get a specific booking by ID"""
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update a booking completely"""
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Partially update a booking"""
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete a booking"""
        return super().destroy(request, *args, **kwargs)