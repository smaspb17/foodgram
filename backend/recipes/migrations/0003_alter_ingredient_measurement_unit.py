# Generated by Django 4.2.4 on 2023-08-22 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(choices=[('гр', 'гр'), ('мл', 'мл'), ('шт', 'шт'), ('ст.л.', 'ст.л.'), ('по вкусу', 'по вкусу'), ('щепотка', 'щепотка')], max_length=255, verbose_name='Единица измерения'),
        ),
    ]
