# Generated by Django 5.0.6 on 2024-06-07 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('Concert', 'Concert'), ('Workshop', 'Workshop'), ('Sport', 'Sport'), ('Theatre', 'Theatre')], max_length=20)),
                ('image', models.ImageField(upload_to='event_images/')),
                ('time', models.DateTimeField()),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
    ]