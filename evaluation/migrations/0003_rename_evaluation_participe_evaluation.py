# Generated by Django 5.0.6 on 2024-07-24 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0002_alter_evaluation_datedebut_alter_evaluation_datefin_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participe',
            old_name='Evaluation',
            new_name='evaluation',
        ),
    ]
