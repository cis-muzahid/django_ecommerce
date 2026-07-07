from django.core.management.base import BaseCommand
from home.models import Banner


class Command(BaseCommand):
    help = 'Generate image variants for existing banners'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=0, help='Limit number of banners processed')

    def handle(self, *args, **options):
        qs = Banner.objects.filter(active=True).order_by('-id')
        limit = options.get('limit') or 0
        if limit > 0:
            qs = qs[:limit]
        total = qs.count()
        self.stdout.write(f'Generating variants for {total} banners...')
        i = 0
        for b in qs:
            i += 1
            self.stdout.write(f'[{i}/{total}] Generating for banner id={b.id} title="{b.title}"')
            try:
                b.generate_variants()
            except Exception as e:
                self.stderr.write(str(e))
        self.stdout.write('Done')
