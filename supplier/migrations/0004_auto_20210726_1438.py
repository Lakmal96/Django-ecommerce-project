# Generated by Django 3.1 on 2021-07-26 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('supplier', '0003_auto_20210726_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierorder',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.supplier'),
        ),
    ]