# Generated by Django 5.1.1 on 2024-12-04 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scannerApp', '0003_rename_barcode_structr_product_info_barcode_structer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_info',
            old_name='barcode_structer',
            new_name='barcode_structure',
        ),
    ]