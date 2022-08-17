# Generated by Django 4.1 on 2022-08-16 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(max_length=200, unique=True)),
                ('api_key', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
