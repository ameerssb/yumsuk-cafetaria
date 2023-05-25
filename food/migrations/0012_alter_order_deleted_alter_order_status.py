# Generated by Django 4.1.5 on 2023-02-12 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0011_alter_order_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, default='Submitted', max_length=100),
        ),
    ]
