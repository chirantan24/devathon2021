# Generated by Django 3.1.7 on 2021-09-18 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20210918_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bio',
            name='blood_group',
            field=models.CharField(choices=[('AB-', 'AB-'), ('O-', 'O-'), ('B-', 'B-'), ('A+', 'A+'), ('AB+', 'AB+'), ('O+', 'O+'), ('B+', 'B+'), ('A-', 'A-')], default='A+', max_length=4),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='gender',
            field=models.CharField(choices=[('Transgender', 'Transgender'), ('Female', 'female'), ('Male', 'male')], default='Male', max_length=20),
        ),
        migrations.AlterField(
            model_name='receptionist',
            name='gender',
            field=models.CharField(choices=[('Transgender', 'Transgender'), ('Female', 'female'), ('Male', 'male')], default='Male', max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('Transgender', 'Transgender'), ('Female', 'female'), ('Male', 'male')], default='Male', max_length=20),
        ),
    ]