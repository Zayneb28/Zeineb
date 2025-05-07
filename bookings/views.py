from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import Trip, Booking, Ticket, Notification
from .forms import BookingForm
from django.conf import settings
import uuid
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'home.html')

def index(request):
    context = {"message": "Hello from template"}
    return render(request, "index.html", context)

def list_trips(request):
    trips = Trip.objects.all().order_by('departure')
    return render(request, 'listTrips.html', {'trips': trips})

def show_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    return render(request, 'showTrip.html', {'trip': trip})

from django.contrib.auth.decorators import login_required

@login_required
def listBookings(request):
    bookings = Booking.objects.all().order_by('-booked_at')
    first_trip = Trip.objects.first()
    default_trip_id = first_trip.id if first_trip else None
    return render(request, 'listBooking.html', {'bookings': bookings, 'default_trip_id': default_trip_id})

def show_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    tickets = booking.tickets.all()
    return render(request, 'showBooking.html', {'booking': booking, 'tickets': tickets})

from django.contrib.auth.decorators import login_required

@login_required
def delete_john_doe_booking(request):
    # Delete all bookings with customer_name "John Doe"
    Booking.objects.filter(customer_name="John Doe").delete()
    messages.success(request, 'All bookings for John Doe have been deleted.')
    return redirect('listBookings')

def add(request):
    trip = Trip.objects.first()
    booking = Booking.objects.create(
        customer_name="John Doe",
        seats=2,
        trip=trip,
        email="johndoe@example.com",
        payment_status=True
    )
    # Create ticket for booking
    ticket_number = str(uuid.uuid4()).replace('-', '').upper()[:20]
    Ticket.objects.create(booking=booking, ticket_number=ticket_number)

    messages.success(request, 'Booking added successfully!')
    return redirect('list_bookings')

from .forms import BookingForm

def add(request):
    trip = Trip.objects.first()  # You can allow selection later if needed

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.trip = trip
            booking.payment_status = True  # Set payment status if needed
            booking.save()

            # Create a ticket
            ticket_number = str(uuid.uuid4()).replace('-', '').upper()[:20]
            Ticket.objects.create(booking=booking, ticket_number=ticket_number)

            messages.success(request, 'Booking added successfully!')
            return redirect('list_bookings', trip_id=trip.id)
    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {'form': form, 'trip': trip, 'available_seats': trip.available_seats})

def edit(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.seats = 3
    booking.save()
    # Create notification
    if request.user.is_authenticated:
        Notification.objects.create(
            user=request.user,
            message=f'Booking {booking.id} has been updated.'
        )
    messages.info(request, 'Booking updated successfully!')
    return redirect('list_bookings')

def remove(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.delete()
    # Create notification
    if request.user.is_authenticated:
        Notification.objects.create(
            user=request.user,
            message=f'Booking {booking_id} has been deleted.'
        )
    messages.warning(request, 'Booking deleted successfully!')

    return redirect('list_bookings')

from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render

from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from .models import Trip
from .forms import BookingForm

@require_http_methods(["GET", "POST"])
def book_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, trip=trip)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.trip = trip
            booking.payment_status = False 
            booking.save()
            return redirect('show_booking', booking_id=booking.id)
    else:
        form = BookingForm(trip=trip)
    return render(request, 'booking_form.html', {'form': form, 'trip': trip})

def notifications(request):
    if not request.user.is_authenticated:
        return redirect('home')
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})

def unread_notifications_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    data = [
        {
            'id': n.id,
            'message': n.message,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for n in unread_notifications
    ]
    return JsonResponse({'notifications': data})

def add_booking(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.trip = trip
            booking.status = 'PENDING'  
            booking.save()
            messages.success(request, "Booking added successfully!")
            return redirect('show_booking', booking.id)
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form, 'trip': trip, 'available_seats': trip.available_seats})

def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("listBookings")
        else:
            messages.info(request, "Incorrect username or password")
    return render(request, "accounts/login.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect("home")

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
         form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})



