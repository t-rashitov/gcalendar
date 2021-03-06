# Generated by Django 3.2.7 on 2021-09-28 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(max_length=100, verbose_name='ID')),
                ('event_type', models.CharField(max_length=100, verbose_name='Тип события')),
                ('summary', models.CharField(blank=True, max_length=2000, verbose_name='Текст')),
                ('start', models.DateTimeField(verbose_name='Дата начала события')),
                ('end', models.DateTimeField(verbose_name='Дата окончания события')),
                ('html_link', models.URLField(verbose_name='URL события')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
            },
        ),
    ]
