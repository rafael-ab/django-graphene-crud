# Generated by Django 3.1.6 on 2021-02-16 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='categories',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
