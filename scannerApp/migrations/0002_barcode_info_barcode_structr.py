# Generated by Django 5.1.1 on 2024-09-24 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scannerApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='barcode_info',
            name='barcode_structr',
            field=models.CharField(default='EAN-13', max_length=100),
        ),
    ]