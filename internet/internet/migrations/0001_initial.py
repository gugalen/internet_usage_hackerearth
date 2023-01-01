# Generated by Django 3.2.6 on 2022-12-30 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsageData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('mac_address', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('usage_time', models.DurationField()),
                ('upload', models.DecimalField(decimal_places=2, max_digits=12)),
                ('download', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
    ]
