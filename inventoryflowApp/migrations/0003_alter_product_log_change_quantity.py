# Generated by Django 5.1.1 on 2024-11-04 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventoryflowApp", "0002_alter_product_log_productinfo_barcodenum_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product_log",
            name="change_quantity",
            field=models.IntegerField(null=True),
        ),
    ]