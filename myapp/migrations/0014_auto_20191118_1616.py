# Generated by Django 2.2.5 on 2019-11-18 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20191118_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.IntegerField(choices=[(3, 'Guest Member'), (1, 'Regular member'), (2, 'Premium Member')], default=1),
        ),
    ]