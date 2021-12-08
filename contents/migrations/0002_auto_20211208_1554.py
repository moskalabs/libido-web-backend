# Generated by Django 3.2.8 on 2021-12-08 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='description',
        ),
        migrations.AddField(
            model_name='content',
            name='dislike_count',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='like_count',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='published_at',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='running_time',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='view_count',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
