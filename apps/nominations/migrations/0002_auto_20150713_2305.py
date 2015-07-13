# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nomination',
            name='reason_to_join_board',
        ),
        migrations.AlterField(
            model_name='nomination',
            name='contribution_info',
            field=models.TextField(default=' Explain in detail about the candidate contribution.\nPlease provide numbered points as much as possible.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nomination',
            name='references',
            field=models.TextField(default='The references themselves must be people who are known by\ntheir work in the Python community. Please enter Name and Email address.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nominationtype',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Whether this  type should be available to public'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nominationtype',
            name='name',
            field=models.CharField(db_index=True, max_length=100, choices=[('Board Member', 'Board Member'), ('Kenneth Gonsalves Award', 'Kenneth Gonsalves Award')]),
            preserve_default=True,
        ),
    ]
