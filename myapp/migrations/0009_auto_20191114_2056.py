# Generated by Django 2.2.5 on 2019-11-15 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20191113_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Member'),
        ),
    ]