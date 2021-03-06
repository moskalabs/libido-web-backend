# Generated by Django 3.2.8 on 2021-12-01 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('content_link_url', models.URLField(max_length=2000)),
                ('thumbnails_url', models.URLField(max_length=2000)),
                ('channel_id', models.CharField(max_length=50, null=True)),
                ('channel_title', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'contents',
            },
        ),
        migrations.CreateModel(
            name='ContentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'content_categories',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='ContentTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.content')),
                ('tags', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.tag')),
            ],
            options={
                'db_table': 'content_tags',
            },
        ),
        migrations.AddField(
            model_name='content',
            name='content_categories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='contents.contentcategory'),
        ),
        migrations.AddField(
            model_name='content',
            name='content_tags',
            field=models.ManyToManyField(related_name='contents', through='contents.ContentTag', to='contents.Tag'),
        ),
    ]
