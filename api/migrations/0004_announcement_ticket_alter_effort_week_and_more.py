# Generated by Django 4.2.2 on 2023-07-08 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(max_length=1000)),
                ('type', models.CharField(choices=[('alert', 'Alert'), ('info', 'Info'), ('warning', 'Warning')], max_length=10)),
                ('starting_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(max_length=1000)),
                ('sender', models.EmailField(max_length=254)),
                ('status', models.CharField(choices=[('open', 'Open'), ('resolved', 'Resolved'), ('closed', 'Closed')], default='open', max_length=10)),
                ('type', models.CharField(choices=[('email', 'Email'), ('web', 'Web')], max_length=10)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='effort',
            name='week',
            field=models.PositiveIntegerField(default=27),
        ),
        migrations.AlterField(
            model_name='habit',
            name='starting_week',
            field=models.PositiveIntegerField(default=27),
        ),
    ]