# Generated by Django 4.2.2 on 2023-06-13 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_goal_color_alter_objective_quarter_alter_task_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='color',
            field=models.CharField(choices=[('blue', 'Blue'), ('red', 'Red'), ('green', 'Green'), ('yellow', 'Yellow'), ('purple', 'Purple'), ('orange', 'Orange'), ('pink', 'Pink'), ('gray', 'Gray'), ('brown', 'Brown'), ('black', 'Black')], max_length=20),
        ),
    ]