# Generated by Django 2.1.3 on 2018-11-14 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_phone',
            field=models.CharField(default='', max_length=13),
        ),
    ]