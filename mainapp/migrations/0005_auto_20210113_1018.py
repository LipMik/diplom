# Generated by Django 3.1.5 on 2021-01-13 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_remove_fulllist_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battery',
            name='name',
        ),
        migrations.RemoveField(
            model_name='drinks',
            name='name',
        ),
        migrations.RemoveField(
            model_name='fulllist',
            name='name',
        ),
        migrations.RemoveField(
            model_name='fulllist',
            name='weight',
        ),
        migrations.RemoveField(
            model_name='milk',
            name='name',
        ),
        migrations.AlterField(
            model_name='battery',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Наименование товара'),
        ),
        migrations.AlterField(
            model_name='drinks',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Наименование товара'),
        ),
        migrations.AlterField(
            model_name='fulllist',
            name='code',
            field=models.DecimalField(decimal_places=0, max_digits=3, verbose_name='Числовой од переработки'),
        ),
        migrations.AlterField(
            model_name='fulllist',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Расшифровка кода'),
        ),
        migrations.AlterField(
            model_name='milk',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Наименование товара'),
        ),
    ]
