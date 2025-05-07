# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'seats']  
        widgets = {
            'seats': forms.NumberInput(attrs={'min': 1}),
        }
    
    def __init__(self, *args, **kwargs):
        self.trip = kwargs.pop('trip', None)
        super().__init__(*args, **kwargs)
        if self.trip:
            self.fields['seats'].widget.attrs['max'] = self.trip.available_seats()
    
    def clean_seats(self):
        seats = self.cleaned_data['seats']
        if self.trip and seats > self.trip.available_seats():
            raise ValidationError(
                f"Only {self.trip.available_seats()} seats available!"
            )
        return seats
