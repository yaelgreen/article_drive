# Generated by Django 2.1.1 on 2018-09-23 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('title_text', models.CharField(max_length=200)),
                ('summary_text', models.CharField(max_length=1000)),
                ('link_text', models.CharField(max_length=200)),
                ('image_url', models.CharField(max_length=200)),
                ('tags', models.CharField(max_length=200)),
                ('state', models.IntegerField(default=0)),
            ],
        ),
    ]
