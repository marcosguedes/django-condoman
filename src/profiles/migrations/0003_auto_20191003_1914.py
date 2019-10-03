# Generated by Django 2.2.5 on 2019-10-03 18:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20191001_2153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proprietorprofile',
            options={'ordering': ('user__name',), 'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AddField(
            model_name='proprietorprofile',
            name='due_exempt_until',
            field=models.DateTimeField(blank=True, help_text="Date until proprietor is exempt from dues. Not publicly available.<br />            Exempt users will be issued exempted dues and won't be notified.             This normally happens when a proprietor is elected manager.", null=True, verbose_name='Exempt from dues until'),
        ),
        migrations.AlterField(
            model_name='proprietorprofile',
            name='vat_number',
            field=models.IntegerField(help_text='Please ensure this number is correct. Numbers only', null=True, validators=[django.core.validators.MaxValueValidator(999999999)], verbose_name='VAT Number'),
        ),
        migrations.CreateModel(
            name='ProprietorBillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('address_1', models.CharField(max_length=400, verbose_name='Address 1')),
                ('address_2', models.CharField(blank=True, max_length=400, verbose_name='Address 2')),
                ('postcode', models.CharField(max_length=100, verbose_name='Post Code')),
                ('city', models.CharField(max_length=100, verbose_name='City / Region')),
                ('country', models.CharField(default='Portugal', max_length=400, verbose_name='Country')),
                ('vat_number', models.CharField(blank=True, help_text='Leave empty if your VAT number is the same one you gave your profile', max_length=9, verbose_name='VAT number')),
                ('proprietor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='profiles.ProprietorProfile')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'ordering': ('proprietor',),
            },
        ),
    ]