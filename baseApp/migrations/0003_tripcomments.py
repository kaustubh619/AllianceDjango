# Generated by Django 2.2.7 on 2020-01-11 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseApp', '0002_auto_20200108_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_image', models.ImageField(blank=True, null=True, upload_to='customer_images')),
                ('customer_name', models.CharField(max_length=200)),
                ('customer_location', models.CharField(max_length=200)),
                ('trip_name', models.CharField(max_length=200)),
                ('customer_comment', models.TextField()),
            ],
        ),
    ]