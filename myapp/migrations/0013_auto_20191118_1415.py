# Generated by Django 2.2.5 on 2019-11-18 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20191118_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.IntegerField(choices=[(2, 'Premium Member'), (1, 'Regular member'), (3, 'Guest Member')], default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
