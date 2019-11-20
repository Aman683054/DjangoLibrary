# Generated by Django 2.2.5 on 2019-11-18 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20191118_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='total_price',
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.IntegerField(choices=[(3, 'Guest Member'), (2, 'Premium Member'), (1, 'Regular member')], default=1),
        ),
    ]
