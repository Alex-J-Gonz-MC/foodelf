# Generated by Django 2.1.7 on 2019-04-14 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_choice_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='calories',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default='N/A', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.FilePathField(default='C:\\Users\\Alex\\Documents\\PythonPractice\\databases\\foodelf\\home\\images', path='C:\\Users\\Alex\\Documents\\PythonPractice\\databases\\foodelf\\home\\images'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='vegan',
            field=models.CharField(default='N/A', max_length=3),
            preserve_default=False,
        ),
    ]
