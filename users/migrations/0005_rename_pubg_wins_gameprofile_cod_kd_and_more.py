# Generated by Django 4.2.18 on 2025-03-09 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_call_of_duty_kd_ratio_gameprofile_brawl_star_trophies_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameprofile',
            old_name='pubg_wins',
            new_name='cod_kd',
        ),
        migrations.RenameField(
            model_name='gameprofile',
            old_name='pubg_username',
            new_name='cod_username',
        ),
    ]
