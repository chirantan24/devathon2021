# Generated by Django 3.1.7 on 2021-09-18 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20210918_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bio',
            name='blood_group',
            field=models.CharField(choices=[('AB+', 'AB+'), ('B+', 'B+'), ('A-', 'A-'), ('B-', 'B-'), ('O-', 'O-'), ('A+', 'A+'), ('O+', 'O+'), ('AB-', 'AB-')], default='A+', max_length=4),
        ),
        migrations.AlterField(
            model_name='bio',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.student'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='gender',
            field=models.CharField(choices=[('Female', 'female'), ('Male', 'male'), ('Transgender', 'Transgender')], default='Male', max_length=20),
        ),
        migrations.AlterField(
            model_name='receptionist',
            name='gender',
            field=models.CharField(choices=[('Female', 'female'), ('Male', 'male'), ('Transgender', 'Transgender')], default='Male', max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('Female', 'female'), ('Male', 'male'), ('Transgender', 'Transgender')], default='Male', max_length=20),
        ),
    ]
