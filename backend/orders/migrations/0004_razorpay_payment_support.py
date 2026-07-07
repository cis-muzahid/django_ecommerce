# Generated migration to support Razorpay payment gateway alongside existing Stripe support.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_paymentevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentevent',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='paymentevent',
            name='payment_gateway',
            field=models.CharField(choices=[('razorpay', 'Razorpay'), ('stripe', 'Stripe'), ('paypal', 'PayPal')], default='razorpay', max_length=50),
        ),
        migrations.AlterField(
            model_name='paymentevent',
            name='stripe_event_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='paymentevent',
            name='currency',
            field=models.CharField(blank=True, default='INR', max_length=12),
        ),
    ]
