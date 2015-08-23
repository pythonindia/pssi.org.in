# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nominations', '0002_auto_20150713_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='nominationtype',
            name='description',
            field=models.TextField(default=b'', verbose_name=b'Short description about nomination type'),
            preserve_default=True,
        ),
    ]
