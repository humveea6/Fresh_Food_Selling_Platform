# Generated by Django 2.2.10 on 2020-03-07 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_emailverifyrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='email',
            field=models.EmailField(max_length=150, verbose_name='邮箱地址'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=150, null=True, verbose_name='邮箱'),
        ),
    ]
