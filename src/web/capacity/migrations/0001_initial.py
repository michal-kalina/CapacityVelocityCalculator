# Generated by Django 3.2.6 on 2021-09-01 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=120)),
                ('surname', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='SprintCapacity',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=120)),
                ('velocity', models.PositiveIntegerField()),
                ('capacity', models.PositiveIntegerField()),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capacity.person')),
            ],
        ),
        migrations.CreateModel(
            name='SprintCapacityPresenceItem',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('date', models.DateTimeField()),
                ('presence', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1)),
                ('sprint_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capacity.sprintcapacity')),
            ],
        ),
    ]
