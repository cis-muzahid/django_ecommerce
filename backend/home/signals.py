from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Banner


@receiver(post_save, sender=Banner)
def generate_banner_variants_on_save(sender, instance, created, **kwargs):
    # Generate variants asynchronously is ideal but keep sync for simplicity
    try:
        instance.generate_variants()
    except Exception:
        pass
