# Generated by Django 3.2.8 on 2021-12-10 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_reset_token_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='day_of_birth',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='nation',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
