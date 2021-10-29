# Generated by Django 3.1.7 on 2021-10-13 13:50

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VariableMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable_name', models.CharField(max_length=100)),
                ('variable_type', models.CharField(choices=[('NM', 'Numeric'), ('CT', 'Categorical'), ('BN', 'Binary'), ('SC', 'Scale')], default='NM', max_length=2)),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VariableResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_date', models.DateField(default=datetime.date.today)),
                ('result_numeric', models.FloatField(blank=True, null=True)),
                ('result_binary', models.BooleanField(blank=True, default=False)),
                ('result_categorical', models.CharField(blank=True, max_length=200, null=True)),
                ('result_scale', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(limit_value=1), django.core.validators.MaxValueValidator(limit_value=10)])),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evolo.variablemaster')),
            ],
            options={
                'ordering': ['-result_date'],
            },
        ),
    ]
