# Generated by Django 3.1.7 on 2021-09-18 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_auto_20210919_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='remaining',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bio',
            name='blood_group',
            field=models.CharField(choices=[('A+', 'A+'), ('B-', 'B-'), ('AB+', 'AB+'), ('O+', 'O+'), ('B+', 'B+'), ('A-', 'A-'), ('O-', 'O-'), ('AB-', 'AB-')], default='A+', max_length=4),
        ),
    ]
