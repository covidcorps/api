# Generated by Django 3.0.5 on 2020-04-05 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corpsmember',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='corpsmemberemail',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='corpsmemberphonenumber',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='locationcontactemail',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='locationcontactphonenumber',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]