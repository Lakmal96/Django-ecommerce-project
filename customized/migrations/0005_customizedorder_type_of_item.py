# Generated by Django 3.1 on 2021-07-19 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customized', '0004_auto_20210719_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='customizedorder',
            name='type_of_item',
            field=models.CharField(choices=[('T-Shirt', 'T-Shirt'), ('Long Sleeve Shirt', 'Long Sleeve Shirt'), ('Short Sleeve Shirt', 'Short Sleeve Shirt')], default='T-Shirt', max_length=25),
        ),
    ]
