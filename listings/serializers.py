from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model - used in nested relationships
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing model with nested host information
    """
    host = UserSerializer(read_only=True)
    host_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'title', 'description', 'price_per_night',
            'location', 'property_type', 'bedrooms', 'bathrooms',
            'max_guests', 'amenities', 'host', 'host_id', 
            'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['listing_id', 'created_at', 'updated_at']
    
    def validate_host_id(self, value):
        """
        Validate that the host_id corresponds to an existing user
        """
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Host with this ID does not exist.")
        return value
    
    def validate_price_per_night(self, value):
        """
        Validate that price is positive
        """
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than 0.")
        return value


class ListingDetailSerializer(ListingSerializer):
    """
    Detailed serializer for Listing with reviews and booking stats
    """
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta(ListingSerializer.Meta):
        fields = ListingSerializer.Meta.fields + ['reviews_count', 'average_rating']
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return None


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model with nested listing and guest information
    """
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.UUIDField(write_only=True)
    guest = UserSerializer(read_only=True)
    guest_id = serializers.IntegerField(write_only=True)
    nights = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'listing', 'listing_id', 'guest', 'guest_id',
            'check_in_date', 'check_out_date', 'number_of_guests',
            'total_price', 'status', 'special_requests', 'nights',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['booking_id', 'created_at', 'updated_at']
    
    def get_nights(self, obj):
        """
        Calculate number of nights for the booking
        """
        return (obj.check_out_date - obj.check_in_date).days
    
    def validate_listing_id(self, value):
        """
        Validate that the listing exists and is available
        """
        try:
            listing = Listing.objects.get(listing_id=value)
            if not listing.is_available:
                raise serializers.ValidationError("This listing is not available for booking.")
        except Listing.DoesNotExist:
            raise serializers.ValidationError("Listing with this ID does not exist.")
        return value
    
    def validate_guest_id(self, value):
        """
        Validate that the guest_id corresponds to an existing user
        """
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Guest with this ID does not exist.")
        return value
    
    def validate(self, data):
        """
        Object-level validation for booking dates and guest capacity
        """
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        number_of_guests = data.get('number_of_guests')
        listing_id = data.get('listing_id')
        
        # Validate dates
        if check_out <= check_in:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        
        # Validate guest capacity
        if listing_id:
            try:
                listing = Listing.objects.get(listing_id=listing_id)
                if number_of_guests > listing.max_guests:
                    raise serializers.ValidationError(
                        f"Number of guests ({number_of_guests}) exceeds maximum capacity ({listing.max_guests})."
                    )
            except Listing.DoesNotExist:
                pass  # Will be caught by listing_id validation
        
        return data
    
    def create(self, validated_data):
        """
        Custom create method to calculate total price
        """
        listing = Listing.objects.get(listing_id=validated_data['listing_id'])
        nights = (validated_data['check_out_date'] - validated_data['check_in_date']).days
        validated_data['total_price'] = listing.price_per_night * nights
        
        return super().create(validated_data)


class BookingListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for booking lists
    """
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    guest_name = serializers.CharField(source='guest.get_full_name', read_only=True)
    nights = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'listing_title', 'guest_name', 'check_in_date',
            'check_out_date', 'nights', 'total_price', 'status', 'created_at'
        ]
    
    def get_nights(self, obj):
        return (obj.check_out_date - obj.check_in_date).days


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model with nested reviewer information
    """
    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.IntegerField(write_only=True)
    listing_id = serializers.UUIDField(write_only=True)
    booking_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Review
        fields = [
            'review_id', 'listing_id', 'reviewer', 'reviewer_id',
            'booking_id', 'rating', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['review_id', 'created_at', 'updated_at']
    
    def validate_listing_id(self, value):
        """
        Validate that the listing exists
        """
        try:
            Listing.objects.get(listing_id=value)
        except Listing.DoesNotExist:
            raise serializers.ValidationError("Listing with this ID does not exist.")
        return value
    
    def validate_reviewer_id(self, value):
        """
        Validate that the reviewer_id corresponds to an existing user
        """
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Reviewer with this ID does not exist.")
        return value
    
    def validate_booking_id(self, value):
        """
        Validate that the booking exists and belongs to the reviewer
        """
        if value:
            try:
                booking = Booking.objects.get(booking_id=value)
                reviewer_id = self.initial_data.get('reviewer_id')
                if reviewer_id and booking.guest_id != reviewer_id:
                    raise serializers.ValidationError("Booking does not belong to this reviewer.")
            except Booking.DoesNotExist:
                raise serializers.ValidationError("Booking with this ID does not exist.")
        return value
    
    def validate(self, data):
        """
        Object-level validation to prevent duplicate reviews
        """
        listing_id = data.get('listing_id')
        reviewer_id = data.get('reviewer_id')
        
        # Check for existing review (only on create)
        if not self.instance:
            existing_review = Review.objects.filter(
                listing_id=listing_id,
                reviewer_id=reviewer_id
            ).exists()
            
            if existing_review:
                raise serializers.ValidationError("You have already reviewed this listing.")
        
        return data