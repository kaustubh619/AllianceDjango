# Generated by Django 2.2.4 on 2020-01-12 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseApp', '0004_auto_20200112_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packages',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='category_packages', to='baseApp.Category'),
        ),
    ]
