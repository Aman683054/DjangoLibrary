# Generated by Django 2.2.5 on 2019-11-18 18:57

from django.db import migrations, models
import myapp.validator


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20191117_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[myapp.validator.maxvaluevalidator, myapp.validator.minvaluevalidator]),
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.IntegerField(choices=[(2, 'Premium Member'), (1, 'Regular member'), (3, 'Guest Member')], default=1),
        ),
    ]