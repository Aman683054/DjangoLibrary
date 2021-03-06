# Generated by Django 2.2.5 on 2019-11-13 21:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_book_num_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.IntegerField(choices=[(3, 'Guest Member'), (2, 'Premium Member'), (1, 'Regular member')], default=1),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer', models.EmailField(max_length=254)),
                ('rating', models.PositiveIntegerField()),
                ('comments', models.TextField(blank=True, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Book')),
            ],
        ),
    ]
