# Generated by Django 3.2.25 on 2024-03-24 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrichment', '0004_enrichmentactivity_attended'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrichmentactivity',
            name='attendance_taken',
            field=models.BooleanField(default=False),
        ),
    ]
