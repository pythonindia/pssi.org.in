# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0005_auto_20141119_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='granttype',
            name='active',
            field=models.BooleanField(verbose_name='Whether this grant type should be available to public', default=True),
            preserve_default=True,
        ),
    ]
