# Generated by Django 3.1.3 on 2020-11-14 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_print_dimension_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendoroffer',
            name='print_job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_offers', to='jobs.printjob'),
        ),
    ]