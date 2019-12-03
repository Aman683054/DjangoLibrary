# Generated by Django 2.2.5 on 2019-12-01 07:30

from django.db import migrations, models
import upload_validator


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_auto_20191201_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Accepted format is .PNG, .JPEG, .JPG', null=True, upload_to='profile', validators=[upload_validator.FileTypeValidator(allowed_types=['image/*'])]),
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.IntegerField(choices=[(3, 'Guest Member'), (2, 'Premium Member'), (1, 'Regular member')], default=1),
        ),
    ]
