# Generated by Django 3.1.3 on 2020-12-11 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20201211_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentsearch',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.agent', unique=True),
        ),
    ]
