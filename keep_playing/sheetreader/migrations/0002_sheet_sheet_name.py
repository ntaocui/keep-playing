# Generated by Django 2.0.1 on 2018-04-07 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheetreader', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheet',
            name='sheet_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
