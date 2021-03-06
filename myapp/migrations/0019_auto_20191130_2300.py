# Generated by Django 2.2.5 on 2019-12-01 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_member_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='Images/'),
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.IntegerField(choices=[(3, 'Guest Member'), (2, 'Premium Member'), (1, 'Regular member')], default=1),
        ),
    ]
