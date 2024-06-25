# Generated by Django 4.2.10 on 2024-06-20 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.CharField(default='', help_text='Slug is a unique name for your blog.', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
