# Generated by Django 5.0.1 on 2024-01-30 16:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_rename_books_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='books.book')),
            ],
        ),
    ]