# Generated by Django 4.1 on 2024-02-10 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kish_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='negative',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='neutral',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='positive',
            field=models.FloatField(null=True),
        ),
    ]
