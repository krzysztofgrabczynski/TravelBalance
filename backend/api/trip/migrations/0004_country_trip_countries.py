# Generated by Django 5.0.4 on 2024-10-01 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0003_alter_trip_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.AddField(
            model_name='trip',
            name='countries',
            field=models.ManyToManyField(blank=True, to='trip.country'),
        ),
    ]