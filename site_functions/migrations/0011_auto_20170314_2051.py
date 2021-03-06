# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 23:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import site_functions.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('site_functions', '0010_remove_article_cpf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='minicurso',
            name='mini_id',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='article',
            name='document',
            field=models.FileField(default=False, upload_to='articles/', validators=[site_functions.validators.validate_article_type]),
        ),
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, related_name='Article_User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='minicurso',
            name='begin',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='modalidade',
            field=models.CharField(choices=[('GRA', 'Estudante de Graduacao'), ('PGR', 'Estudante de Pos-Graduacao'), ('PRO', 'Profissional')], default=False, max_length=3),
        ),
    ]
