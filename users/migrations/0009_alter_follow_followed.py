# Generated by Django 3.2.8 on 2022-01-26 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_follow_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='followed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_by_followed', to='users.user'),
        ),
    ]
