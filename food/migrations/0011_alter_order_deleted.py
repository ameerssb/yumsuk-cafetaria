# Generated by Django 4.1.5 on 2023-02-12 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_alter_order_payment_type_alter_order_total_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deleted',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
