# Generated by Django 5.1.1 on 2024-12-04 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scannerApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_info',
            old_name='barcode_structure',
            new_name='barcode_structr',
        ),
        migrations.RenameField(
            model_name='product_info',
            old_name='product_image',
            new_name='product_img',
        ),
        migrations.RenameField(
            model_name='product_info',
            old_name='current_quantity',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='product_info',
            name='initial_stock',
        ),
    ]
