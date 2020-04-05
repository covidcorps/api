# Generated by Django 3.0.5 on 2020-04-05 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_account_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='corpsmember',
            name='category',
            field=models.CharField(choices=[('DOCTOR', 'Doctor'), ('NURSE', 'Nurse'), ('RESPIRATORY', 'Respiratory Specialist'), ('ORDERLY', 'Orderly'), ('PA', 'Physicians Assistant'), ('NP', 'Nurse Practicioner'), ('PSYCHOLOGIST', 'Psychologist'), ('PSYCHIATRIST', 'Psychiatrist')], default='DOCTOR', max_length=30),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('ACCEPTED', 'ACCEPTED'), ('ENROUTE', 'ENROUTE'), ('ONSITE', 'ONSITE'), ('COMPLETE', 'COMPLETE')], max_length=10),
        ),
        migrations.AlterField(
            model_name='corpsmember',
            name='address2',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='corpsmember',
            name='middle_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='corpsmember',
            name='prefix',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='corpsmember',
            name='state',
            field=models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('DC', 'District of Columbia'), ('NC', 'North Carolina'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2),
        ),
        migrations.AlterField(
            model_name='corpsmember',
            name='suffix',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='corpsmemberemail',
            name='preferred',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='corpsmemberphonenumber',
            name='preferred',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='corpsmemberphonenumber',
            name='sms_ok',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='address2',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='location',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='location',
            name='state',
            field=models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('DC', 'District of Columbia'), ('NC', 'North Carolina'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2),
        ),
        migrations.AlterField(
            model_name='locationcontact',
            name='middle_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='locationcontact',
            name='prefix',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='locationcontact',
            name='suffix',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='locationcontactemail',
            name='preferred',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='locationcontactphonenumber',
            name='preferred',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='locationcontactphonenumber',
            name='sms_ok',
            field=models.BooleanField(default=False),
        ),
    ]
