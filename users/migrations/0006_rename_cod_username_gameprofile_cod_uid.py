# Generated by Django 4.2.18 on 2025-03-11 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_pubg_wins_gameprofile_cod_kd_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameprofile',
            old_name='cod_username',
            new_name='cod_uid',
        ),
    ]
