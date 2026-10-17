from django.core.management.base import BaseCommand

from core import ledger


class Command(BaseCommand):
    help = 'Pay out every seller whose balance is above PAYOUT_THRESHOLD (also runs weekly through Celery beat).'

    def handle(self, *args, **options):
        payouts = ledger.run_weekly_payouts()
        for p in payouts:
            self.stdout.write(f'Paid seller {p.seller_id}: {p.amount}')
        self.stdout.write(self.style.SUCCESS(f'{len(payouts)} payout(s) made.'))
