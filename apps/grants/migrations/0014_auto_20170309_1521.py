# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import grants.models


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0013_auto_20170306_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localconfrequest',
            name='note',
        ),
        migrations.AddField(
            model_name='localconfrequest',
            name='upload',
            field=models.FileField(default='', upload_to=grants.models.upload_to_path),
            preserve_default=False,
        ),
    ]
