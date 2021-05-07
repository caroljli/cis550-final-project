# Generated by Django 3.2 on 2021-05-07 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0005_delete_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('authors', models.CharField(max_length=800)),
                ('average_rating', models.IntegerField()),
            ],
            options={
                'db_table': 'BOOKS_EXTENSIVE',
            },
        ),
    ]