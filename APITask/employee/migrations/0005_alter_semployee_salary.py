# Generated by Django 5.1.1 on 2024-09-30 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_job_alter_femployee_status_alter_semployee_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semployee',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]