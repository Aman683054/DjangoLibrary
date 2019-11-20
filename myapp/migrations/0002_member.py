# Generated by Django 2.2.5 on 2019-09-30 15:51

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('status', models.IntegerField(choices=[(1, 'Regular member'), (2, 'Premium Member'), (3, 'Guest Member')], default=1)),
                ('address', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=20)),
                ('province', models.CharField(default='ON', max_length=2)),
                ('last_renewal', models.DateField(default=django.utils.timezone.now)),
                ('auto_renew', models.BooleanField(default=True)),
                ('borrowed_books', models.ManyToManyField(blank=True, to='myapp.Book')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
