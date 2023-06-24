# Generated by Django 4.2.2 on 2023-06-24 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_habit_color_habit_expected_effort'),
    ]

    operations = [
        migrations.AddField(
            model_name='effortlog',
            name='year',
            field=models.PositiveIntegerField(default=2023),
        ),
        migrations.AddField(
            model_name='habit',
            name='year',
            field=models.PositiveIntegerField(default=2023),
        ),
        migrations.AlterField(
            model_name='habit',
            name='color',
            field=models.CharField(default='rose', max_length=255),
        ),
    ]
