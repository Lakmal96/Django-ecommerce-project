# Generated by Django 3.1 on 2021-07-03 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210606_0949'),
        ('orders', '0002_auto_20210704_0053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variation',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]
