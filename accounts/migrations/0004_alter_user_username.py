# Generated by Django 4.2.1 on 2023-06-17 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_code_remove_user_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=70, null=True, verbose_name='username'),
        ),
    ]
