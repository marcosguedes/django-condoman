# Generated by Django 2.2.5 on 2019-09-30 22:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CondominiumConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condominium_fee', models.DecimalField(decimal_places=2, default='10.0', help_text='Value in Euros', max_digits=9, verbose_name='Condominium Fees')),
                ('condominium_payment_day', models.PositiveSmallIntegerField(default=1, help_text='Payment Day. Choose a value from 1 to 27 in order to avoid issues with February and leaping years', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(27)], verbose_name='Day')),
            ],
            options={
                'verbose_name': 'Condominium General Configuration',
            },
        ),
    ]
