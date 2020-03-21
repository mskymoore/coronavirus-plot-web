# Generated by Django 3.0.4 on 2020-03-21 00:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DateSeries',
            fields=[
                ('date_retrieved', models.DateTimeField(default=django.utils.timezone.now, primary_key=True, serialize=False)),
                ('date_series', models.BinaryField(default=[])),
            ],
        ),
        migrations.CreateModel(
            name='SelectionString',
            fields=[
                ('selection_string', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province_state', models.CharField(default='', max_length=100)),
                ('region_country', models.CharField(default='', max_length=100)),
                ('selection_string', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='corona_plots.SelectionString')),
            ],
        ),
        migrations.CreateModel(
            name='CountSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series_type', models.CharField(max_length=100)),
                ('count_series', models.BinaryField(default=[])),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corona_plots.Location')),
                ('selection_string', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corona_plots.SelectionString')),
            ],
        ),
    ]