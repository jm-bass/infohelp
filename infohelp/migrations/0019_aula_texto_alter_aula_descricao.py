# Generated by Django 5.1.3 on 2025-02-03 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infohelp', '0018_aula_link_alter_aula_descricao'),
    ]

    operations = [
        migrations.AddField(
            model_name='aula',
            name='texto',
            field=models.TextField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='aula',
            name='descricao',
            field=models.TextField(max_length=200),
        ),
    ]
