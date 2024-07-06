from django.core.management.base import BaseCommand
from checker.models import PaymentService


class Command(BaseCommand):
    help = 'Seeds the database with initial data'
    data = [
        {
            'name': 'TELEBIRR',
            'identifier': 'TELE_BIRR',
            'is_active': True
        },
        {
            'name': 'YENE_PAY',
            'identifier': 'YENE_PAY',
            'is_active': True
        },
        {
            'name': 'CHAPA',
            'identifier': 'CHAPA',
            'is_active': True
        }
    ]

    def handle(self, *args, **kwargs):
        for data in self.data:
            try:
                PaymentService.objects.create(**data)
                self.stdout.write(self.style.SUCCESS(f"Payment Service '{data['name']}' created successfully."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error seeding Payment Services: {e}"))