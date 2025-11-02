from django.core.management.base import BaseCommand
import csv
from netflix.models import NetflixShow

class Command(BaseCommand):
    help = 'Import NetFlix.csv into the database'

    def handle(self, *args, **kwargs):
        with open('NetFlix.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                NetflixShow.objects.update_or_create(
                    show_id=row['show_id'],
                    defaults={
                        'type': row['type'],
                        'title': row['title'],
                        'director': row.get('director', ''),
                        'cast': row.get('cast', ''),
                        'country': row.get('country', ''),
                        'date_added': row.get('date_added', ''),
                        'release_year': int(row['release_year']),
                        'rating': row['rating'],
                        'duration': row['duration'],
                        'listed_in': row['genres'],
                        'description': row['description'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported NetFlix.csv'))
