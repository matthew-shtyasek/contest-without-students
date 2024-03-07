# Generated by Django 4.2 on 2024-03-07 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('file_id', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'file',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FilePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'file_permission',
                'managed': False,
            },
        ),
    ]
