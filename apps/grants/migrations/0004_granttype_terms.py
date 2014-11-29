# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0003_auto_20141119_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='granttype',
            name='terms',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
