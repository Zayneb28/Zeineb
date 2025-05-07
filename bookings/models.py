from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Trip(models.Model):
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    TRANSPORT_CHOICES = [
        ('train', 'Train'),
        ('plane', 'Plane'),
    ]
    transport_type = models.CharField(max_length=10, choices=TRANSPORT_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    total_seats = models.PositiveIntegerField(default=50)
    
    @property
    def available_seats(self):
        booked_seats = sum(booking.seats for booking in self.booking_set.filter(payment_status=True))
        return self.total_seats - booked_seats
    
    class Meta:
        verbose_name = "Trip"
        verbose_name_plural = "Trips"
        ordering = ['departure_time']
        
    def __str__(self):
        return f"{self.departure} to {self.destination} ({self.transport_type})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    customer_name = models.CharField(max_length=64)
    seats = models.IntegerField(default=1)
    booked_at = models.DateTimeField(auto_now_add=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    email = models.EmailField()  
    payment_status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        
        
    def __str__(self):
        return f"Booking {self.booking_reference} for {self.trip}"

class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='tickets')
    ticket_number = models.CharField(max_length=20, unique=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"Ticket {self.ticket_number} for Booking {self.booking.id}"


