# Generated by Django 2.2.5 on 2019-10-21 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20191021_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.IntegerField(choices=[(1, 'Regular member'), (3, 'Guest Member'), (2, 'Premium Member')], default=1),
        ),
    ]
