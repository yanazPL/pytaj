# Generated by Django 3.0.6 on 2020-08-17 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_answer_is_best_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='stats',
            name='karma',
            field=models.BigIntegerField(default=0),
        ),
    ]
