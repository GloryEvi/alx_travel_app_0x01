from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from decimal import Decimal
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=30,
            help='Number of bookings to create (default: 30)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=25,
            help='Number of reviews to create (default: 25)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(
                self.style.WARNING('Clearing existing data...')
            )
            self.clear_data()

        # Create sample data
        users = self.create_users(options['users'])
        listings = self.create_listings(options['listings'], users)
        bookings = self.create_bookings(options['bookings'], listings, users)
        self.create_reviews(options['reviews'], listings, users, bookings)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded database with:\n'
                f'- {len(users)} users\n'
                f'- {len(listings)} listings\n'
                f'- {len(bookings)} bookings\n'
                f'- {options["reviews"]} reviews'
            )
        )

    def clear_data(self):
        """Clear existing data from models"""
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        # Don't delete superuser accounts
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('Existing data cleared.')

    def create_users(self, count):
        """Create sample users"""
        self.stdout.write(f'Creating {count} users...')
        
        users = []
        sample_users = [
            ('john_doe', 'John', 'Doe', 'john@example.com'),
            ('jane_smith', 'Jane', 'Smith', 'jane@example.com'),
            ('mike_johnson', 'Mike', 'Johnson', 'mike@example.com'),
            ('sarah_wilson', 'Sarah', 'Wilson', 'sarah@example.com'),
            ('david_brown', 'David', 'Brown', 'david@example.com'),
            ('emma_davis', 'Emma', 'Davis', 'emma@example.com'),
            ('alex_miller', 'Alex', 'Miller', 'alex@example.com'),
            ('lisa_garcia', 'Lisa', 'Garcia', 'lisa@example.com'),
            ('ryan_taylor', 'Ryan', 'Taylor', 'ryan@example.com'),
            ('anna_anderson', 'Anna', 'Anderson', 'anna@example.com'),
        ]
        
        for i in range(min(count, len(sample_users))):
            username, first_name, last_name, email = sample_users[i]
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'is_active': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        
        # Create additional users if needed
        for i in range(len(sample_users), count):
            user, created = User.objects.get_or_create(
                username=f'user_{i+1}',
                defaults={
                    'first_name': f'User',
                    'last_name': f'{i+1}',
                    'email': f'user{i+1}@example.com',
                    'is_active': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        
        return users

    def create_listings(self, count, users):
        """Create sample listings"""
        self.stdout.write(f'Creating {count} listings...')
        
        sample_listings = [
            {
                'title': 'Luxury Downtown Apartment',
                'description': 'Beautiful modern apartment in the heart of the city with stunning views and premium amenities.',
                'price': 150.00,
                'location': 'New York, NY',
                'property_type': 'apartment',
                'bedrooms': 2,
                'bathrooms': 2,
                'max_guests': 4,
                'amenities': 'WiFi, Air Conditioning, Kitchen, Parking, Pool, Gym'
            },
            {
                'title': 'Cozy Beach House',
                'description': 'Charming beach house just steps from the ocean. Perfect for a relaxing getaway.',
                'price': 200.00,
                'location': 'Miami, FL',
                'property_type': 'house',
                'bedrooms': 3,
                'bathrooms': 2,
                'max_guests': 6,
                'amenities': 'WiFi, Beach Access, Kitchen, Parking, BBQ Grill'
            },
            {
                'title': 'Mountain View Villa',
                'description': 'Spectacular villa with panoramic mountain views and luxury furnishings.',
                'price': 350.00,
                'location': 'Aspen, CO',
                'property_type': 'villa',
                'bedrooms': 4,
                'bathrooms': 3,
                'max_guests': 8,
                'amenities': 'WiFi, Fireplace, Kitchen, Parking, Hot Tub, Mountain Views'
            },
            {
                'title': 'Urban Studio Loft',
                'description': 'Modern studio loft in trendy neighborhood with exposed brick and high ceilings.',
                'price': 80.00,
                'location': 'Portland, OR',
                'property_type': 'studio',
                'bedrooms': 1,
                'bathrooms': 1,
                'max_guests': 2,
                'amenities': 'WiFi, Kitchen, Exposed Brick, High Ceilings'
            },
            {
                'title': 'Lakefront Cabin',
                'description': 'Rustic cabin on the lake perfect for fishing and outdoor activities.',
                'price': 120.00,
                'location': 'Lake Tahoe, CA',
                'property_type': 'cabin',
                'bedrooms': 2,
                'bathrooms': 1,
                'max_guests': 4,
                'amenities': 'WiFi, Lake Access, Kitchen, Parking, Fireplace, Fishing'
            }
        ]
        
        listings = []
        for i in range(count):
            if i < len(sample_listings):
                data = sample_listings[i]
            else:
                # Generate additional listings with variations
                base_data = sample_listings[i % len(sample_listings)]
                data = base_data.copy()
                data['title'] = f"Property {i+1} - {base_data['title']}"
                data['price'] = round(random.uniform(50, 400), 2)
                data['bedrooms'] = random.randint(1, 5)
                data['bathrooms'] = random.randint(1, 3)
                data['max_guests'] = data['bedrooms'] * 2
            
            listing = Listing.objects.create(
                title=data['title'],
                description=data['description'],
                price_per_night=Decimal(str(data['price'])),
                location=data['location'],
                property_type=data['property_type'],
                bedrooms=data['bedrooms'],
                bathrooms=data['bathrooms'],
                max_guests=data['max_guests'],
                amenities=data['amenities'],
                host=random.choice(users),
                is_available=True
            )
            listings.append(listing)
        
        return listings

    def create_bookings(self, count, listings, users):
        """Create sample bookings"""
        self.stdout.write(f'Creating {count} bookings...')
        
        bookings = []
        statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        
        for i in range(count):
            listing = random.choice(listings)
            guest = random.choice(users)
            
            # Ensure guest is not the host
            while guest == listing.host:
                guest = random.choice(users)
            
            # Generate random dates
            start_date = date.today() + timedelta(days=random.randint(-30, 60))
            nights = random.randint(1, 14)
            end_date = start_date + timedelta(days=nights)
            
            # Random number of guests within listing capacity
            num_guests = random.randint(1, listing.max_guests)
            
            # Calculate total price
            total_price = listing.price_per_night * nights
            
            booking = Booking.objects.create(
                listing=listing,
                guest=guest,
                check_in_date=start_date,
                check_out_date=end_date,
                number_of_guests=num_guests,
                total_price=total_price,
                status=random.choice(statuses),
                special_requests='Standard check-in' if random.random() > 0.3 else 'Early check-in requested'
            )
            bookings.append(booking)
        
        return bookings

    def create_reviews(self, count, listings, users, bookings):
        """Create sample reviews"""
        self.stdout.write(f'Creating {count} reviews...')
        
        sample_comments = [
            "Amazing place! Everything was perfect and the host was very accommodating.",
            "Great location and beautiful property. Would definitely stay again!",
            "The apartment was clean and well-equipped. Highly recommended.",
            "Perfect for our family vacation. Kids loved the amenities.",
            "Stunning views and excellent service. Worth every penny!",
            "Cozy and comfortable. Felt like home away from home.",
            "Great value for money. The location was perfect for exploring the city.",
            "Beautiful property with all the amenities we needed.",
            "The host was responsive and the place was exactly as described.",
            "Wonderful stay! The property exceeded our expectations."
        ]
        
        created_reviews = 0
        attempts = 0
        max_attempts = count * 3  # Avoid infinite loop
        
        while created_reviews < count and attempts < max_attempts:
            attempts += 1
            listing = random.choice(listings)
            reviewer = random.choice(users)
            
            # Ensure reviewer is not the host and hasn't already reviewed this listing
            if (reviewer == listing.host or 
                Review.objects.filter(listing=listing, reviewer=reviewer).exists()):
                continue
            
            # Try to find a completed booking for this reviewer and listing
            booking = None
            completed_bookings = Booking.objects.filter(
                listing=listing,
                guest=reviewer,
                status='completed'
            )
            if completed_bookings.exists():
                booking = random.choice(completed_bookings)
            
            Review.objects.create(
                listing=listing,
                reviewer=reviewer,
                booking=booking,
                rating=random.randint(3, 5),  # Mostly positive reviews
                comment=random.choice(sample_comments)
            )
            created_reviews += 1
        
        self.stdout.write(f'Created {created_reviews} reviews')