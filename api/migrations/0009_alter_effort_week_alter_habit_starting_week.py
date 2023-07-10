# Generated by Django 4.2.2 on 2023-07-10 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_habit_ending_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='effort',
            name='week',
            field=models.PositiveIntegerField(default=28),
        ),
        migrations.AlterField(
            model_name='habit',
            name='starting_week',
            field=models.PositiveIntegerField(default=28),
        ),
    ]
