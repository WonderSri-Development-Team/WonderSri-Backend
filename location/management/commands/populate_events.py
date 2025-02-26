# location/management/commands/populate_events.py
from django.core.management.base import BaseCommand
from location.models import Event, Venue
from datetime import datetime

class Command(BaseCommand):
    help = 'Populate the events database'

    def handle(self, *args, **kwargs):
        # Example data
        events_data = [
            {
                'title': 'Music Concert',
                'description': 'A live music concert.',
                'venue_id': 1,  # Assuming you have a venue with ID 1
                'start_date': datetime(2025, 3, 1, 18, 0),
                'end_date': datetime(2025, 3, 1, 21, 0),
                'price': 20.00,
                'image': None,  # Add image path if needed
                'is_active': True,
            },
            # Add more events as needed
        ]

        for event_data in events_data:
            event = Event(**event_data)
            event.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully added event: {event.title}'))
