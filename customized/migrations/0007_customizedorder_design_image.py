# Generated by Django 3.1 on 2021-07-19 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customized', '0006_remove_customizedorder_type_of_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='customizedorder',
            name='design_image',
            field=models.ImageField(blank=True, upload_to='customized_orders/'),
        ),
    ]