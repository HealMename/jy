# Generated by Django 2.1.3 on 2018-11-07 18:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sop', '0002_auto_20181107_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water', models.CharField(max_length=2)),
                ('times', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='admins',
            name='detail',
            field=models.CharField(default='', max_length=62),
        ),
        migrations.AddField(
            model_name='users',
            name='user_expend',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=60),
        ),
        migrations.AddField(
            model_name='users',
            name='user_income',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=60),
        ),
    ]