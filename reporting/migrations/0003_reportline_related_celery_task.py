# Generated by Django 3.2 on 2021-12-04 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reporting", "0002_reportline"),
    ]

    operations = [
        migrations.AddField(
            model_name="reportline",
            name="related_celery_task",
            field=models.CharField(max_length=130, null=True),
        ),
    ]
