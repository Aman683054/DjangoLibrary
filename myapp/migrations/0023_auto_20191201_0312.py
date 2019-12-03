# Generated by Django 2.2.5 on 2019-12-01 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_auto_20191201_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='avatar',
            field=models.FileField(blank=True, help_text='Accepted format are .PNG, .JPEG, .JPG', null=True, upload_to='profile'),
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.IntegerField(choices=[(1, 'Regular member'), (2, 'Premium Member'), (3, 'Guest Member')], default=1),
        ),
    ]
