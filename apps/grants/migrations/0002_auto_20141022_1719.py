# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grantrequest',
            name='talk_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
